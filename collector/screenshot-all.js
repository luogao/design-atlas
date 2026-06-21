#!/usr/bin/env node
/**
 * 批量截图脚本 — 对每个设计系统的 HTML demo 截图生成 preview.png
 * 用法: node collector/screenshot-all.js
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ATLAS = path.resolve(__dirname, '..');
const RDS = '/Users/gaogao/Documents/projects/retro-design-system';
const manifest = JSON.parse(fs.readFileSync(path.join(ATLAS, 'manifest.json'), 'utf8'));

async function main() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1200, height: 800 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  let done = 0;
  let failed = 0;

  for (const sys of manifest.systems) {
    const sysDir = path.join(ATLAS, 'systems', sys.id);
    const outPath = path.join(sysDir, 'preview.png');

    // 跳过已有截图的
    if (fs.existsSync(outPath)) {
      console.log(`  ✓ ${sys.id} (skip, exists)`);
      done++;
      continue;
    }

    // 找源 HTML
    const relPath = sys.source.original_path; // styles/XX-slug/
    const htmlPath = path.join(RDS, relPath, 'index.html');

    if (!fs.existsSync(htmlPath)) {
      console.log(`  ✗ ${sys.id} — HTML not found: ${htmlPath}`);
      failed++;
      continue;
    }

    try {
      const fileUrl = 'file://' + htmlPath;
      await page.goto(fileUrl, { waitUntil: 'networkidle', timeout: 10000 });
      // 给 web font 一点时间
      await page.waitForTimeout(500);
      await page.screenshot({ path: outPath, fullPage: false });
      console.log(`  ✓ ${sys.id} → preview.png (${++done}/${manifest.systems.length})`);
    } catch (err) {
      console.log(`  ✗ ${sys.id} — ${err.message}`);
      failed++;
    }
  }

  await browser.close();
  console.log(`\nDone: ${done} success, ${failed} failed`);

  // 更新 manifest — 加 preview 字段
  for (const sys of manifest.systems) {
    const previewPath = path.join(ATLAS, 'systems', sys.id, 'preview.png');
    if (fs.existsSync(previewPath)) {
      sys.preview = `systems/${sys.id}/preview.png`;
    }
  }
  fs.writeFileSync(path.join(ATLAS, 'manifest.json'), JSON.stringify(manifest, null, 2));
  console.log('manifest.json updated with preview paths');
}

main().catch(console.error);
