#!/usr/bin/env node
/**
 * Re-shoot a single system's preview from a given URL.
 * Usage: node collector/rescreenshot.js <system-id> <url>
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ATLAS = path.resolve(__dirname, '..');
const [id, url] = process.argv.slice(2);
if (!id || !url) { console.error('usage: node rescreenshot.js <id> <url>'); process.exit(1); }
const out = path.join(ATLAS, 'systems', id, 'preview.png');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  page.on('console', () => {});
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
  } catch (e) {
    console.log('  ↳ networkidle timeout, fallback load');
    try { await page.goto(url, { waitUntil: 'load', timeout: 45000 }); }
    catch (e2) { console.log('  ↳ load failed too: ' + e2.message); }
  }
  await page.waitForTimeout(1500);
  const title = await page.title();
  const text = (await page.evaluate(() => document.body.innerText || '')).slice(0, 120).replace(/\s+/g, ' ');
  await page.screenshot({ path: out, fullPage: false });
  console.log(`  title="${title}"`);
  console.log(`  text="${text}"`);
  console.log(`  ✅ ${out} (${Math.round(fs.statSync(out).size / 1024)} KB)`);
  await browser.close();
})();
