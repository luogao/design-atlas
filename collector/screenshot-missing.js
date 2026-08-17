#!/usr/bin/env node
/**
 * 截取缺失 preview.png 的 auto-collected 系统的 demo_url
 * 用法: node collector/screenshot-missing.js
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ATLAS = path.resolve(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(ATLAS, 'manifest.json'), 'utf8'));

// 只处理 preview.png 不存在的
const targets = manifest.systems.filter(s => {
  const out = path.join(ATLAS, 'systems', s.id, 'preview.png');
  return s.preview && !fs.existsSync(out);
});

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1200, height: 800 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  let ok = 0, fail = 0;
  for (const s of targets) {
    const outPath = path.join(ATLAS, 'systems', s.id, 'preview.png');
    const url = s.demo_url;
    if (!url) { console.log(`  ✗ ${s.id} — no demo_url`); fail++; continue; }

    try {
      console.log(`  → ${s.id}: ${url}`);
      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      } catch (e) {
        // networkidle 超时（长连接/分析 beacon 持续发包），退回 load 事件后截图
        console.log(`    ↳ networkidle 超时，退回 load…`);
        await page.goto(url, { waitUntil: 'load', timeout: 45000 });
      }
      await page.waitForTimeout(1500); // 等 web font / 渲染
      await page.screenshot({ path: outPath, fullPage: false });
      const sz = fs.statSync(outPath).size;
      console.log(`  ✓ ${s.id} → preview.png (${(sz/1024).toFixed(0)} KB)`);
      ok++;
    } catch (err) {
      console.log(`  ✗ ${s.id} — ${err.message}`);
      fail++;
    }
  }

  await browser.close();
  console.log(`\nDone: ${ok} success, ${fail} failed`);
})();
