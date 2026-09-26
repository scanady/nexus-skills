// Visual QA: render exact timeline moments into labelled 2×2 contact sheets (four frames per image read).
// Usage: node shots.mjs 3.2 12 18.5 40        → shots/sheet-01.jpg (+ more sheets if >4 times)
//        node shots.mjs --auto                 → per scene: just after entry, middle, just before exit
//        node shots.mjs --scene recap,hook     → the same three moments for the named scene(s)
//        node shots.mjs 12.4 --full            → also writes shots/t12.4.jpg at full resolution (for detail checks)
// Prints console errors and the text visible at each moment.
import fs from "node:fs";
import { args, jobPath } from "./lib/config.mjs";
import { launch, openPage } from "./lib/browser.mjs";

const a = args();
const browser = await launch();
const { page, errors, meta } = await openPage(browser);
let times = a._.map(Number).filter(Number.isFinite);
if (a.auto || a.scene) {
  const want = a.scene ? new Set(String(a.scene).split(",")) : null;
  for (const s of meta.scenes.filter(s => !want || want.has(s.name))) {
    const len = s.end - s.start;
    times.push(s.start + Math.min(0.9, len * 0.2), s.start + len * 0.55, s.end - Math.min(0.5, len * 0.1));
  }
}
times = [...new Set(times.map(t => +Math.min(Math.max(0, t), meta.dur - 0.01).toFixed(2)))].sort((x, y) => x - y);
if (!times.length) { console.error("give times in seconds, or --auto, or --scene <name>"); process.exit(1); }
fs.mkdirSync(jobPath("shots"), { recursive: true });

for (let g = 0; g < times.length; g += 4) {
  const group = times.slice(g, g + 4);
  const res = await page.evaluate(({ group, full }) => {
    const src = window.__canvas, W = src.width, H = src.height;
    const sheet = document.createElement("canvas"); sheet.width = W; sheet.height = H;
    const c = sheet.getContext("2d"); c.fillStyle = "#222"; c.fillRect(0, 0, W, H);
    const info = [], fulls = {};
    group.forEach((t, k) => {
      window.__render(t);
      if (full) fulls[t] = src.toDataURL("image/jpeg", 0.9);
      const x = (k % 2) * W / 2, y = Math.floor(k / 2) * H / 2;
      c.drawImage(src, x, y, W / 2, H / 2);
      const label = `${t.toFixed(2)}s  ${window.__active(t).join(" → ")}`;
      c.font = "bold 26px sans-serif"; const w = c.measureText(label).width;
      c.fillStyle = "rgba(0,0,0,.72)"; c.fillRect(x + 8, y + 8, w + 20, 40);
      c.fillStyle = "#ffe066"; c.fillText(label, x + 18, y + 38);
      info.push({ t, scenes: window.__active(t), text: window.__text().filter(b => b.alpha > 0.3).map(b => b.str) });
    });
    c.strokeStyle = "#000"; c.lineWidth = 4; c.beginPath(); c.moveTo(W / 2, 0); c.lineTo(W / 2, H); c.moveTo(0, H / 2); c.lineTo(W, H / 2); c.stroke();
    return { sheet: sheet.toDataURL("image/jpeg", 0.85), info, fulls };
  }, { group, full: !!a.full });
  const name = `shots/sheet-${String(g / 4 + 1).padStart(2, "0")}.jpg`;
  fs.writeFileSync(jobPath(name), Buffer.from(res.sheet.split(",")[1], "base64"));
  for (const [t, d] of Object.entries(res.fulls)) fs.writeFileSync(jobPath(`shots/t${t}.jpg`), Buffer.from(d.split(",")[1], "base64"));
  console.log(name);
  for (const i of res.info) console.log(`  ${i.t.toFixed(2)}s [${i.scenes.join(", ") || "NO SCENE"}] ${i.text.map(s => JSON.stringify(s.slice(0, 50))).join(" | ")}`);
}
const uniq = [...new Set(errors)];
if (uniq.length) { console.log(`\nconsole errors (${uniq.length}):`); uniq.slice(0, 30).forEach(e => console.log("  " + e)); }
await browser.close();
