// Download Google Fonts as woff2 so build.mjs can embed them (renders never touch the network).
// Usage: node fonts.mjs "Caveat:wght@700" "Nunito:wght@400;800" [--subsets latin,latin-ext | all]
// Order matters: DATA.fontFamilies[0] is the first family, [1] the second, and so on.
// Out: fonts/*.woff2, fonts.json
import fs from "node:fs";
import { args, jobPath, writeJson, die, env } from "./lib/config.mjs";

const a = args();
const families = a._;
if (!families.length) die('usage: node fonts.mjs "Family:wght@400;700" ["Other+Family"] [--subsets latin,latin-ext|all]');
const subsets = String(a.subsets ?? env("EXPLAINER_FONT_SUBSETS", "latin,latin-ext")).split(",");
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36";
fs.mkdirSync(jobPath("fonts"), { recursive: true });

const out = [];
for (const fam of families) {
  const url = `https://fonts.googleapis.com/css2?family=${fam.replace(/ /g, "+")}&display=block`;
  const res = await fetch(url, { headers: { "User-Agent": UA } });
  if (!res.ok) die(`Google Fonts ${res.status} for "${fam}": check the family name and axis syntax (e.g. "Caveat:wght@700")`);
  const css = await res.text();
  const blocks = [...css.matchAll(/(?:\/\*\s*([^*]+?)\s*\*\/\s*)?@font-face\s*\{([^}]*)\}/g)];
  let kept = 0;
  for (const [, subset = "default", body] of blocks) {
    if (!subsets.includes("all") && !subsets.includes(subset) && subset !== "default") continue;
    const prop = n => (body.match(new RegExp(`${n}:\\s*([^;]+);`)) || [])[1]?.trim();
    const family = prop("font-family").replace(/['"]/g, "");
    const src = (prop("src").match(/url\(([^)]+)\)/) || [])[1];
    const weight = prop("font-weight") ?? "400", style = prop("font-style") ?? "normal";
    const file = `fonts/${family.replace(/\W+/g, "")}-${weight.replace(/\s+/g, "_")}-${style}-${subset.replace(/\W+/g, "")}.woff2`;
    const r = await fetch(src);
    if (!r.ok) die(`font download failed: ${src}`);
    fs.writeFileSync(jobPath(file), Buffer.from(await r.arrayBuffer()));
    out.push({ family, weight, style, subset, unicodeRange: prop("unicode-range"), file });
    kept++;
  }
  if (!kept) die(`"${fam}" has no faces in subsets ${subsets.join(",")}: try --subsets all`);
  console.log(`${fam}: ${kept} face(s)`);
}
writeJson("fonts.json", out);
console.log(`fonts.json: families in order → ${[...new Set(out.map(f => f.family))].join(", ")}`);
