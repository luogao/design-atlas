#!/usr/bin/env node
/** Verify the three new systems render in the gallery (card + preview image loads). */
const { chromium } = require('playwright');
const path = require('path');
const ATLAS = path.resolve(__dirname, '..');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  const base = process.env.BASE_URL || ('file://' + path.join(ATLAS, 'gallery', 'index.html'));
  await page.goto(base, { waitUntil: 'load' });
  await page.waitForTimeout(2500);
  const info = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('*')).filter(
      e => e.className && String(e.className).includes('card'));
    const text = document.body.innerText;
    const imgs = Array.from(document.images).map(i => ({ src: i.currentSrc || i.src, w: i.naturalWidth }));
    return {
      cardCount: cards.length,
      hasMilligram: text.includes('milligram'),
      hasMini: text.toLowerCase().includes('mini.css'),
      hasWing: /\bwing\b/i.test(text),
      brokenImgs: imgs.filter(i => i.w === 0).length,
      totalImgs: imgs.length,
      sample: text.slice(0, 200),
    };
  });
  console.log(JSON.stringify(info, null, 1));
  // screenshot the card grid area
  await page.screenshot({ path: '/Users/gaogao/.hermes/cache/scratch/gallery_check.png', fullPage: false });
  await browser.close();
})();
