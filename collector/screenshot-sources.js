#!/usr/bin/env node
// Screenshot demo pages of new design sources
const { chromium } = require('playwright');

const targets = [
  {
    id: 'nes-css',
    name: 'NES.css',
    url: 'https://nostalgic-css.github.io/NES.css/',
    wait: 'networkidle'
  },
  {
    id: '98css',
    name: '98.css',
    url: 'https://jdan.github.io/98.css/',
    wait: 'networkidle'
  },
  {
    id: 'xp-css',
    name: 'XP.css',
    url: 'https://botoxparty.github.io/XP.css/',
    wait: 'networkidle'
  },
  {
    id: '7-css',
    name: '7.css',
    url: 'https://khang-nd.github.io/7.css/',
    wait: 'networkidle'
  },
  {
    id: 'neobrutalism-css',
    name: 'NeoBrutalismCSS',
    url: 'https://matifandy8.github.io/NeoBrutalismCSS/',
    wait: 'networkidle'
  },
  {
    id: 'cyberpunk-css',
    name: 'cyberpunk-css',
    url: 'https://alddesign.github.io/cyberpunk-css/demo/',
    wait: 'networkidle'
  }
];

const OUT_DIR = '/Users/gaogao/Documents/Hermes/design-atlas/_vendor/screenshots';

(async () => {
  const fs = require('fs');
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });

  for (const target of targets) {
    const page = await browser.newPage({
      viewport: { width: 1200, height: 800 },
      deviceScaleFactor: 2
    });

    try {
      console.log(`Capturing ${target.id}...`);
      await page.goto(target.url, { waitUntil: target.wait, timeout: 30000 });
      await page.waitForTimeout(1500); // extra settle time

      const outPath = `${OUT_DIR}/${target.id}.png`;
      await page.screenshot({ path: outPath, type: 'png' });
      console.log(`  ✅ ${target.id} -> ${outPath}`);
    } catch (err) {
      console.error(`  ❌ ${target.id}: ${err.message}`);
    }

    await page.close();
  }

  await browser.close();
  console.log('\nDone!');
})();
