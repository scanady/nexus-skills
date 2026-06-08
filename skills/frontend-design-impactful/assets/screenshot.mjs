// Full-page screenshots at multiple widths, for the render-and-critique loop.
//
// Usage:
//   node screenshot.mjs <url> <outDir>
//   node screenshot.mjs http://localhost:3000 ./.screens
//   node screenshot.mjs file:///absolute/path/to/index.html ./.screens
//
// Setup:
//   npm i -D playwright
//   npx playwright install chromium
//
// Then open the PNGs in ./.screens with the view tool and critique against
// references/render-and-critique.md.

import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";

const url = process.argv[2] || "http://localhost:3000";
const outDir = process.argv[3] || "./.screens";
const widths = [360, 768, 1280, 1440];

await mkdir(outDir, { recursive: true });

// Try Playwright's bundled chromium first; fall back to a system Chrome/Chromium/Edge.
async function launch() {
  try {
    return await chromium.launch();
  } catch (e) {
    console.warn("Bundled chromium unavailable, trying system Chrome channel...");
    return await chromium.launch({ channel: "chrome" });
  }
}

const browser = await launch();
try {
  for (const width of widths) {
    const page = await browser.newPage({
      viewport: { width, height: 900 },
      deviceScaleFactor: 2,
    });
    await page.goto(url, { waitUntil: "networkidle" });

    // Let entry sequences settle.
    await page.waitForTimeout(1200);

    // Scroll the full height to trigger scroll-linked and lazy content, then reset.
    await page.evaluate(async () => {
      const step = window.innerHeight;
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 120));
      }
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(400);

    const file = `${outDir}/screen-${width}.png`;
    await page.screenshot({ path: file, fullPage: true });
    console.log(`saved ${file}`);
    await page.close();
  }
} finally {
  await browser.close();
}
