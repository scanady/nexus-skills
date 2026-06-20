#!/usr/bin/env node
/*
 * build-site.js
 *
 * Assembles the GitHub Pages distribution under dist/site/:
 *   - index.html                            ← landing page with install commands
 *   - skill-catalog.html                    ← catalog browser (existing)
 *   - pack-manager.html                     ← pack manager (existing)
 *   - skill-catalog.json                    ← raw catalog
 *   - skill-catalog-summary.md              ← summary doc
 *   - marketplace/.claude-plugin/marketplace.json   ← published marketplace
 *   - plugins/<pack>.zip                    ← per-pack downloadable bundles
 *   - plugins/manifest.json                 ← pack manifest (machine readable)
 *
 * Prerequisite: run `node bin/build-plugins.js` first so dist/plugins/ exists.
 *
 * Usage:
 *   node bin/build-site.js
 */

const childProcess = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DIST_PLUGINS = path.join(ROOT, 'dist', 'plugins');
const SITE_DIR = path.join(ROOT, 'dist', 'site');
const SITE_PLUGINS_DIR = path.join(SITE_DIR, 'plugins');
const SITE_MARKETPLACE_DIR = path.join(SITE_DIR, 'marketplace', '.claude-plugin');

function copyFile(src, dest) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

function rmDir(dir) {
  if (fs.existsSync(dir)) fs.rmSync(dir, { recursive: true, force: true });
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function rootVersion() {
  try {
    return readJson(path.join(ROOT, 'package.json')).version || '0.0.0';
  } catch {
    return '0.0.0';
  }
}

function zipDirectory(sourceDir, outZip) {
  // Cross-platform: prefer Node's built-in via child_process to PowerShell/zip.
  // We use PowerShell on Windows, zip on POSIX. This script is invoked by CI on Linux runners,
  // so the zip path will be used in practice. Local dev on Windows also works.
  if (process.platform === 'win32') {
    const psCmd = `Compress-Archive -Path '${sourceDir}\\*' -DestinationPath '${outZip}' -Force`;
    childProcess.execSync(`powershell -NoProfile -Command "${psCmd}"`, { stdio: 'inherit' });
  } else {
    // -j would junk paths; we want to keep the pack folder name as the top-level entry
    const parent = path.dirname(sourceDir);
    const base = path.basename(sourceDir);
    childProcess.execSync(`cd "${parent}" && zip -rq "${outZip}" "${base}"`, { stdio: 'inherit' });
  }
}

function buildIndexHtml(manifest, version) {
  const packRows = manifest.packs.map(p => `
        <tr>
          <td><code>${p.pluginName}</code></td>
          <td>${p.skills.length}</td>
          <td><a href="plugins/${p.name}.zip" download>${p.name}.zip</a></td>
          <td><code>nyld-nexus-skills install --pack ${p.name}</code></td>
        </tr>`).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>nyld-nexus-skills</title>
<style>
  :root { --bg:#0f1117; --surface:#1a1d27; --surface2:#242736; --border:#343848;
          --text:#e2e4f0; --muted:#8b90a8; --accent:#6c72f7; }
  * { box-sizing: border-box; }
  body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
         background:var(--bg); color:var(--text); line-height:1.55; }
  .wrap { max-width:980px; margin:0 auto; padding:48px 24px; }
  h1 { font-size:2.2rem; margin:0 0 4px; letter-spacing:-0.02em; }
  h1 span { color:var(--accent); }
  .tag { color:var(--muted); margin:0 0 32px; }
  .links { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:40px; }
  .links a { background:var(--surface); border:1px solid var(--border); color:var(--text);
             text-decoration:none; padding:10px 16px; border-radius:8px; font-size:0.92rem; }
  .links a:hover { border-color:var(--accent); color:var(--accent); }
  h2 { margin-top:40px; font-size:1.3rem; }
  pre { background:var(--surface); border:1px solid var(--border); border-radius:8px;
        padding:16px; overflow-x:auto; font-size:0.85rem; }
  code { font-family:"SF Mono","Consolas",monospace; font-size:0.88em; }
  table { width:100%; border-collapse:collapse; margin:16px 0; font-size:0.9rem; }
  th, td { text-align:left; padding:10px 12px; border-bottom:1px solid var(--border); }
  th { color:var(--muted); font-weight:600; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.05em; }
  td a { color:var(--accent); text-decoration:none; }
  td a:hover { text-decoration:underline; }
  .meta { color:var(--muted); font-size:0.82rem; margin-top:48px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>nyld-<span>nexus</span>-skills</h1>
  <p class="tag">Agentic skills, prompts, agents, and instructions for AI development platforms — v${version}</p>

  <div class="links">
    <a href="skill-catalog.html">📚 Skill Catalog</a>
    <a href="pack-manager.html">📦 Pack Manager</a>
    <a href="skill-catalog.json">📄 Raw Catalog JSON</a>
    <a href="skill-catalog-summary.md">📝 Summary</a>
  </div>

  <h2>Install via CLI</h2>
  <pre>npm exec --yes --package=git+https://git.nylcloud.com/Direct/nyld-nexus-skills.git#main -- nyld-nexus-skills install</pre>

  <h2>Install a specific pack</h2>
  <pre>nyld-nexus-skills install --pack marketing
nyld-nexus-skills install --pack tech --pack data</pre>

  <h2>Install as a Claude plugin</h2>
  <p>Add this repo as a Claude Code marketplace, then install any pack plugin:</p>
  <pre>/plugin marketplace add https://git.nylcloud.com/Direct/nyld-nexus-skills.git
/plugin install nexus-marketing</pre>

  <h2>Download a pack bundle</h2>
  <table>
    <thead><tr><th>Plugin</th><th>Skills</th><th>Download</th><th>CLI</th></tr></thead>
    <tbody>${packRows}
    </tbody>
  </table>

  <p class="meta">Generated ${manifest.generated_at} · <a href="plugins/manifest.json" style="color:var(--muted)">manifest.json</a></p>
</div>
</body>
</html>
`;
}

function main() {
  if (!fs.existsSync(DIST_PLUGINS)) {
    console.error('❌ dist/plugins/ not found. Run `node bin/build-plugins.js` first.');
    process.exit(1);
  }

  const version = rootVersion();
  const manifest = readJson(path.join(DIST_PLUGINS, 'manifest.json'));

  rmDir(SITE_DIR);
  fs.mkdirSync(SITE_DIR, { recursive: true });

  // 1. Copy browser assets
  copyFile(path.join(ROOT, 'skill-catalog.html'), path.join(SITE_DIR, 'skill-catalog.html'));
  copyFile(path.join(ROOT, 'pack-manager.html'), path.join(SITE_DIR, 'pack-manager.html'));
  copyFile(path.join(ROOT, 'skill-catalog.json'), path.join(SITE_DIR, 'skill-catalog.json'));
  const summaryPath = path.join(ROOT, 'skill-catalog-summary.md');
  if (fs.existsSync(summaryPath)) {
    copyFile(summaryPath, path.join(SITE_DIR, 'skill-catalog-summary.md'));
  }

  // 2. Marketplace JSON (so users can point Claude at the Pages URL)
  copyFile(
    path.join(ROOT, '.claude-plugin', 'marketplace.json'),
    path.join(SITE_MARKETPLACE_DIR, 'marketplace.json')
  );

  // 3. Per-pack zips
  fs.mkdirSync(SITE_PLUGINS_DIR, { recursive: true });
  for (const pack of manifest.packs) {
    const src = path.join(DIST_PLUGINS, pack.name);
    const out = path.join(SITE_PLUGINS_DIR, `${pack.name}.zip`);
    if (fs.existsSync(out)) fs.rmSync(out);
    zipDirectory(src, out);
  }
  copyFile(path.join(DIST_PLUGINS, 'manifest.json'), path.join(SITE_PLUGINS_DIR, 'manifest.json'));

  // 4. Landing page
  fs.writeFileSync(path.join(SITE_DIR, 'index.html'), buildIndexHtml(manifest, version), 'utf8');

  // 5. .nojekyll so GitHub Pages serves files starting with _
  fs.writeFileSync(path.join(SITE_DIR, '.nojekyll'), '', 'utf8');

  console.log(`Site built at ${path.relative(ROOT, SITE_DIR)}/ (${manifest.packs.length} pack zips)`);
}

if (require.main === module) {
  try {
    main();
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}

module.exports = { main };
