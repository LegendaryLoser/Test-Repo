// Captures scene.html frame-by-frame to PNGs via headless Chromium.
// Usage: node capture.cjs <outDir> [probe]
//   probe mode renders only a set of key frames for composition checks.
const fs = require('fs');
const path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

(async () => {
  const outDir = process.argv[2];
  const probe = process.argv[3] === 'probe';
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => { console.error('PAGE ERROR:', e.message); process.exitCode = 1; });
  await page.goto('file://' + path.join(__dirname, 'scene.html'));

  const total = await page.evaluate('window.TOTAL_FRAMES');
  const wanted = probe
    ? new Set([60, 150, 250, 330, 352, 365, 390, 460, 500, 530, 545, 560, 600, 640, 655, 700, 760])
    : null;

  const t0 = Date.now();
  for (let i = 0; i < total; i++) {
    const data = await page.evaluate(`window.renderFrame(${i})`);
    if (!wanted || wanted.has(i)) {
      fs.writeFileSync(path.join(outDir, `f_${String(i).padStart(4, '0')}.png`),
        Buffer.from(data.slice(data.indexOf(',') + 1), 'base64'));
    }
    if (i % 100 === 0) console.log(`frame ${i}/${total} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  }
  console.log('markers:', await page.evaluate('window.getMarkers()'));
  console.log(`done in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  await browser.close();
})();
