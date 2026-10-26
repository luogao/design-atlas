#!/usr/bin/env node
/** Screenshot gallery cards matching a search term. Usage: node shot-search.js "milligram" out.png */
const { chromium } = require('playwright');
const path = require('path');
const ATLAS = path.resolve(__dirname, '..');
const term = process.argv[2] || 'milligram';
const out = process.argv[3] || '/Users/gaogao/.hermes/cache/scratch/search-shot.png';

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1100 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto(process.env.BASE_URL || 'http://127.0.0.1:8811/gallery/index.html', { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  const input = await page.$('input[type="text"], input[type="search"], .search-input, input[placeholder]');
  if (input) { await input.fill(term); await page.waitForTimeout(1200); }
  await page.evaluate(() => window.scrollTo(0, 520));
  await page.waitForTimeout(1200);
  const n = await page.evaluate(() => document.querySelectorAll('.system-card, .card').length);
  console.log('cards after search:', n);
  await page.screenshot({ path: out });
  console.log('saved', out);
  await browser.close();
})();
