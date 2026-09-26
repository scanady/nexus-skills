// Headless Chromium via Playwright. Falls back to an installed Chrome or Edge when the
// Playwright browser download is missing (common on locked-down Windows machines).
import { pathToFileURL } from "node:url";
import { config, jobPath, die } from "./config.mjs";

const FLAGS = ["--autoplay-policy=no-user-gesture-required", "--font-render-hinting=none", "--force-color-profile=srgb", "--hide-scrollbars", "--disable-lcd-text"];

export async function launch() {
  let chromium;
  try { ({ chromium } = await import("playwright")); }
  catch { die("playwright is not installed: run `npm install` in the skill's scripts/ folder"); }
  const tries = config.chromePath ? [{ executablePath: config.chromePath }] : [{}, { channel: "chrome" }, { channel: "msedge" }];
  let err;
  for (const t of tries) {
    try { return await chromium.launch({ headless: true, args: FLAGS, ...t }); } catch (e) { err = e; }
  }
  die(`cannot launch a browser: ${err?.message?.split("\n")[0]}\nRun \`npx playwright install chromium\` in the skill's scripts/ folder, or set EXPLAINER_CHROME_PATH.`);
}

// Open the built page in render mode and wait for the engine. Collects console errors.
export async function openPage(browser, { file = "out.html", scale = 1 } = {}) {
  const { width, height } = config.video;
  const page = await browser.newPage({ viewport: { width: Math.round(width * scale), height: Math.round(height * scale) }, deviceScaleFactor: 1 });
  const errors = [];
  page.on("console", m => { if (m.type() === "error" || m.type() === "warning") errors.push(m.text()); });
  page.on("pageerror", e => errors.push("PAGE ERROR " + e.message));
  await page.goto(pathToFileURL(jobPath(file)).href + "?render", { waitUntil: "load" });
  try { await page.waitForFunction("window.__ready === true", null, { timeout: 90000 }); }
  catch { die(`engine never became ready:\n${errors.join("\n") || "(no console output)"}`); }
  const meta = await page.evaluate(() => window.__meta);
  return { page, errors, meta };
}
