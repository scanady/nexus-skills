#!/usr/bin/env node
/**
 * Layer validator for scroll scenes. Static check of an HTML file plus the local
 * CSS and JS it links. No dependencies. Node 18+.
 *
 * Usage:
 *   node scripts/validate-layers.mjs index.html [more.html ...] [--json] [--strict]
 *
 * Exit codes: 0 pass, 1 errors found (or warnings with --strict), 2 bad usage.
 *
 * Checks (E = error, W = warning)
 *   Structure  E html lang · E exactly one <main> · E exactly one <h1> · E img alt
 *              E h1 not aria-hidden · W skip link
 *   Layers     E at least one scene · E each scene has 3+ depth layers
 *              E data-depth is an integer 0-5 · E decorative layers aria-hidden
 *              W split-text elements without aria-label
 *   Motion     E prefers-reduced-motion in CSS · W matchMedia reduced check in JS
 *              W no mobile/touch fallback · W content hidden before JS runs
 *   Cost       E global will-change · W layout properties in keyframes/transition
 *              W more than 80 animated elements
 *   Scroll     W competing scroll libraries · W scroll lock or wheel preventDefault
 *              W mandatory scroll-snap
 *   Supply     W external script without integrity
 *
 * It reads source text. It cannot see runtime state. Treat it as a gate for
 * the common mistakes, then test in a browser and on a real device.
 */

import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const LAYOUT_PROPS = 'width|height|top|left|right|bottom|margin(?:-[a-z]+)?|padding(?:-[a-z]+)?|font-size|letter-spacing';
const ANIMATED_LIMIT = 80;

// ---------- args ----------
const argv = process.argv.slice(2);
const flags = new Set(argv.filter((a) => a.startsWith('--')));
const files = argv.filter((a) => !a.startsWith('--'));
if (flags.has('--help') || files.length === 0) {
  console.error('Usage: node scripts/validate-layers.mjs <file.html> [...] [--json] [--strict]');
  process.exit(files.length === 0 && !flags.has('--help') ? 2 : 0);
}

// ---------- source loading ----------
const isRemote = (u) => /^(?:[a-z]+:)?\/\//i.test(u) || u.startsWith('data:');

function loadSources(htmlPath) {
  const html = readFileSync(htmlPath, 'utf8');
  const base = dirname(htmlPath);
  let css = '';
  let js = '';

  for (const m of html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)) css += m[1] + '\n';
  for (const m of html.matchAll(/<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)) js += m[1] + '\n';

  const linked = [];
  for (const m of html.matchAll(/<link\b[^>]*>/gi)) {
    const a = attrs(m[0]);
    if (/stylesheet/i.test(a.rel || '') && a.href && !isRemote(a.href)) linked.push(['css', a.href]);
  }
  for (const m of html.matchAll(/<script\b[^>]*>/gi)) {
    const a = attrs(m[0]);
    if (a.src && !isRemote(a.src)) linked.push(['js', a.src]);
  }
  const missing = [];
  for (const [kind, href] of linked) {
    const p = resolve(base, href.split(/[?#]/)[0]);
    if (!existsSync(p)) { missing.push(href); continue; }
    const text = readFileSync(p, 'utf8');
    if (kind === 'css') css += text + '\n'; else js += text + '\n';
  }
  return { html, css, js, missing };
}

// ---------- html parsing (small, tolerant) ----------
function attrs(tag) {
  const out = {};
  const body = tag.replace(/^<\/?[a-zA-Z][\w:-]*/, '').replace(/\/?>$/, '');
  for (const m of body.matchAll(/([^\s=/>"']+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) {
    out[m[1].toLowerCase()] = m[2] ?? m[3] ?? m[4] ?? '';
  }
  return out;
}

function parse(html) {
  const clean = html
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, (m) => m.match(/^<[^>]+>/)[0] + `</${m.match(/^<(\w+)/)[1]}>`);
  const root = { tag: '#root', attrs: {}, parent: null, children: [], text: '' };
  let cur = root;
  const re = /<(\/?)([a-zA-Z][\w:-]*)([^>]*)>|([^<]+)/g;
  for (const m of clean.matchAll(re)) {
    if (m[4] !== undefined) { cur.text += m[4]; continue; }
    const [raw, closing, name] = m;
    const tag = name.toLowerCase();
    if (closing) {
      let n = cur;
      while (n && n.tag !== tag) n = n.parent;
      if (n && n.parent) cur = n.parent;
      continue;
    }
    const node = { tag, attrs: attrs(raw), parent: cur, children: [], text: '' };
    cur.children.push(node);
    if (!VOID.has(tag) && !/\/>$/.test(raw)) cur = node;
  }
  return root;
}

const walk = (n, fn) => { fn(n); n.children.forEach((c) => walk(c, fn)); };
const hasClass = (n, re) => re.test(n.attrs.class || '');
const ariaHiddenSelfOrAncestor = (n) => { for (let p = n; p; p = p.parent) if (p.attrs?.['aria-hidden'] === 'true') return true; return false; };
const isElementHidden = (n) => ariaHiddenSelfOrAncestor(n) || 'hidden' in n.attrs;

function matchBraces(src, startIdx) {
  let depth = 0;
  for (let i = startIdx; i < src.length; i++) {
    if (src[i] === '{') depth++;
    else if (src[i] === '}' && --depth === 0) return i;
  }
  return src.length - 1;
}

// ---------- checks ----------
function run(file) {
  const { html, css, js, missing } = loadSources(file);
  const root = parse(html);
  const nodes = [];
  walk(root, (n) => n !== root && nodes.push(n));
  const findings = [];
  const add = (level, id, message, fix) => findings.push({ level, id, message, fix });
  const pass = [];

  const cssNoComments = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const jsNoComments = js.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:])\/\/.*$/gm, '$1');

  for (const href of missing) add('W', 'asset-missing', `Linked file not found, not checked: ${href}`, 'Fix the path or check the file by hand.');

  // Structure
  const htmlEl = nodes.find((n) => n.tag === 'html');
  htmlEl?.attrs.lang ? pass.push('html lang set') : add('E', 'lang', '<html> has no lang attribute.', 'Add lang="en" (or the page language).');

  const mains = nodes.filter((n) => n.tag === 'main');
  if (mains.length === 1) pass.push('one <main>');
  else add(mains.length ? 'W' : 'E', 'main', `Found ${mains.length} <main> landmarks.`, 'Use exactly one <main id="main-content">.');

  const h1s = nodes.filter((n) => n.tag === 'h1');
  if (h1s.length === 1) pass.push('one <h1>');
  else add('E', 'h1', `Found ${h1s.length} <h1> elements.`, 'Use exactly one <h1> as the real page heading.');
  h1s.filter((h) => ariaHiddenSelfOrAncestor(h)).forEach(() =>
    add('E', 'h1-hidden', 'An <h1> is inside aria-hidden content.', 'Decorative ghost text may be aria-hidden. The real heading may not.'));

  const imgs = nodes.filter((n) => n.tag === 'img');
  const noAlt = imgs.filter((i) => !('alt' in i.attrs));
  noAlt.length
    ? add('E', 'img-alt', `${noAlt.length} of ${imgs.length} <img> have no alt attribute (${noAlt.slice(0, 3).map((i) => i.attrs.src || '?').join(', ')}).`,
          'Meaningful images get descriptive alt. Decorative images get alt="".')
    : pass.push(`all ${imgs.length} <img> have alt`);

  const skip = nodes.some((n) => n.tag === 'a' && /^#/.test(n.attrs.href || '') && /skip/i.test((n.attrs.class || '') + n.text));
  skip ? pass.push('skip link') : add('W', 'skip-link', 'No skip-to-content link.', 'First element in <body>: <a href="#main-content" class="skip-link">Skip to main content</a>.');

  // Layers
  const scenes = nodes.filter((n) => hasClass(n, /(^|\s)scene(\s|$)/) || 'data-scene' in n.attrs);
  if (!scenes.length) add('E', 'scene', 'No scene found (class="scene" or data-scene).', 'Wrap each scroll section in <section class="scene" data-scene="name">.');

  let layerTotal = 0;
  for (const scene of scenes) {
    const layers = [];
    walk(scene, (n) => n !== scene && 'data-depth' in n.attrs && layers.push(n));
    layerTotal += layers.length;
    const name = scene.attrs['data-scene'] || scene.attrs['aria-label'] || scene.attrs.class || scene.tag;
    if (layers.length < 3) add('E', 'scene-layers', `Scene "${name}" has ${layers.length} depth layer(s). Need 3+.`, 'Add layers: background (0), main object (3), text (4) at minimum.');
  }

  const allDepth = nodes.filter((n) => 'data-depth' in n.attrs);
  allDepth.filter((n) => !/^[0-5]$/.test(n.attrs['data-depth'])).forEach((n) =>
    add('E', 'depth-value', `data-depth="${n.attrs['data-depth']}" is not an integer 0-5.`, 'Use one of the six depth levels.'));

  const unhiddenDecor = allDepth.filter((n) => /^[015]$/.test(n.attrs['data-depth']) && !ariaHiddenSelfOrAncestor(n));
  if (unhiddenDecor.length) add('E', 'decor-aria', `${unhiddenDecor.length} decorative layer(s) (depth 0, 1, 5) are not aria-hidden.`, 'Add aria-hidden="true" to those layers.');
  const decoClass = nodes.filter((n) => hasClass(n, /glow|particle|sparkle|deco/) && n.tag !== 'html' && !ariaHiddenSelfOrAncestor(n) && !allDepth.includes(n));
  if (decoClass.length) add('W', 'decor-class', `${decoClass.length} element(s) with glow/particle/deco classes are not aria-hidden.`, 'Hide decorative nodes from assistive tech.');

  const splitNoLabel = nodes.filter((n) => (hasClass(n, /split/) || 'data-split' in n.attrs) && !n.attrs['aria-label'] && !isElementHidden(n));
  if (splitNoLabel.length) add('W', 'split-label', `${splitNoLabel.length} split-text element(s) have no aria-label.`, 'Put the full text in aria-label on the parent, aria-hidden on the fragments.');

  // Motion
  const hasReducedCss = /prefers-reduced-motion/.test(cssNoComments);
  hasReducedCss ? pass.push('prefers-reduced-motion in CSS') : add('E', 'reduced-css', 'No prefers-reduced-motion rule found in CSS.', 'Make reduced motion the base or add a reduce block. See references/scroll-accessibility.md.');

  const usesScrollLib = /gsap|ScrollTrigger|framer-motion|lenis|locomotive/i.test(html + js);
  if (usesScrollLib && !/matchMedia\([^)]*prefers-reduced-motion|gsap\.matchMedia|useReducedMotion/.test(js + html))
    add('W', 'reduced-js', 'Scroll library in use but no reduced-motion check found in JS.', 'Gate JS animation with gsap.matchMedia() or matchMedia("(prefers-reduced-motion: reduce)").');

  if (allDepth.length && usesScrollLib && !/pointer:\s*coarse|max-width\s*:|min-width\s*:|perf-lite|gsap\.matchMedia/.test(js + cssNoComments))
    add('W', 'mobile', 'Depth parallax with no touch or small-screen fallback.', 'Branch on (pointer: coarse) or width. Use lite mode on phones.');

  const hiddenBeforeJs = /\[data-animate[^\]]*\][^{}]*\{[^}]*opacity\s*:\s*0\b/.test(cssNoComments) || /\.(?:reveal|fade-in|will-animate)\s*\{[^}]*opacity\s*:\s*0\b/.test(cssNoComments);
  const jsGuard = /\.js[\s.{>[:]|no-js|\.no-js/.test(cssNoComments) || /<noscript|class="[^"]*\bno-js\b|classList\.add\(['"]js['"]\)/.test(html + js);
  if (hiddenBeforeJs && !jsGuard)
    add('W', 'hidden-before-js', 'CSS hides animated content (opacity: 0) with no .js guard.', 'Hide only under a .js class set by a script in <head>. Content must read without JS.');

  // Cost
  /(^|[},\s])\*\s*(?:,[^{]*)?\{[^}]*will-change/.test(cssNoComments)
    ? add('E', 'will-change-global', 'will-change set on the universal selector.', 'Remove it. Apply will-change only to elements about to animate.')
    : pass.push('no global will-change');

  const layoutHits = new Set();
  for (const m of cssNoComments.matchAll(/@keyframes\s+([\w-]+)\s*\{/g)) {
    const open = m.index + m[0].length - 1;
    const body = cssNoComments.slice(open, matchBraces(cssNoComments, open) + 1);
    if (new RegExp(`(?:^|[;{\\s])(?:${LAYOUT_PROPS})\\s*:`).test(body)) layoutHits.add(`@keyframes ${m[1]}`);
  }
  for (const m of cssNoComments.matchAll(/transition(?:-property)?\s*:\s*([^;}]*)/g)) {
    if (new RegExp(`\\b(?:${LAYOUT_PROPS})\\b`).test(m[1])) layoutHits.add(`transition: ${m[1].trim().slice(0, 40)}`);
    else if (/^\s*all\b/.test(m[1])) layoutHits.add('transition: all');
  }
  layoutHits.size
    ? add('W', 'layout-anim', `Layout-triggering properties animated: ${[...layoutHits].slice(0, 4).join('; ')}.`, 'Animate transform and opacity. See references/scroll-performance.md.')
    : pass.push('no layout properties in keyframes or transitions');

  const animated = nodes.filter((n) => 'data-animate' in n.attrs || 'data-depth' in n.attrs || hasClass(n, /(^|\s)float(-loop)?(\s|$)/)).length;
  animated > ANIMATED_LIMIT
    ? add('W', 'animated-count', `${animated} animated elements. Over ${ANIMATED_LIMIT} risks dropped frames.`, 'Merge decorative sprites, cut particles, lazy-init far scenes.')
    : pass.push(`${animated} animated elements (limit ${ANIMATED_LIMIT})`);

  // Scroll behaviour
  const libs = [
    /locomotive/i.test(html + js) && 'Locomotive Scroll',
    /ScrollTrigger|gsap/i.test(html + js) && 'GSAP ScrollTrigger',
    /framer-motion|useScroll/i.test(html + js) && 'Framer Motion',
  ].filter(Boolean);
  if (libs.includes('Locomotive Scroll') && libs.length > 1) add('W', 'competing-libs', `Competing scroll systems: ${libs.join(' + ')}.`, 'Pick one primary library, or wire them together on purpose.');
  else if (libs.includes('GSAP ScrollTrigger') && libs.includes('Framer Motion')) add('W', 'competing-libs', 'GSAP and Framer Motion both drive scroll.', 'Pick one primary library.');

  if (/(?:document\.)?(?:body|documentElement)\.style\.overflow\s*=\s*['"]hidden/.test(jsNoComments) || /(?:html|body)\s*\{[^}]*overflow\s*:\s*hidden/.test(cssNoComments))
    add('W', 'scroll-lock', 'Scroll lock on html/body found.', 'Allowed only for a short loader. Always release it, including on error.');
  if (/(?:wheel|touchmove)[\s\S]{0,200}preventDefault|preventDefault[\s\S]{0,200}(?:wheel|touchmove)|Observer\.create\([\s\S]{0,300}preventDefault\s*:\s*true/.test(jsNoComments))
    add('W', 'scroll-hijack', 'preventDefault on wheel or touch input. This hijacks scroll.', 'Enhance native scroll. Use CSS scroll-snap proximity or soft ScrollTrigger snap.');
  if (/scroll-snap-type\s*:[^;]*mandatory/.test(cssNoComments)) add('W', 'snap-mandatory', 'scroll-snap-type: mandatory found.', 'Use proximity. Mandatory can trap users in tall sections.');

  // Supply chain
  const cdn = nodes.filter((n) => n.tag === 'script' && /^(?:https?:)?\/\//.test(n.attrs.src || '') && !('integrity' in n.attrs));
  if (cdn.length) add('W', 'sri', `${cdn.length} external script(s) without integrity: ${cdn.slice(0, 2).map((n) => n.attrs.src).join(', ')}.`, 'Pin an exact version and add integrity + crossorigin, or bundle locally.');

  return { file, pass, findings };
}

// ---------- report ----------
const reports = files.map((f) => {
  try { return run(f); } catch (e) { return { file: f, pass: [], findings: [{ level: 'E', id: 'read', message: `Could not read: ${e.message}`, fix: 'Check the path.' }] }; }
});

if (flags.has('--json')) {
  console.log(JSON.stringify(reports, null, 2));
} else {
  for (const r of reports) {
    console.log(`\nLayer validation: ${r.file}\n${'-'.repeat(60)}`);
    r.pass.forEach((p) => console.log(`PASS  ${p}`));
    for (const f of r.findings) {
      console.log(`${f.level === 'E' ? 'ERROR' : 'WARN '} [${f.id}] ${f.message}`);
      console.log(`      fix: ${f.fix}`);
    }
    const e = r.findings.filter((f) => f.level === 'E').length;
    const w = r.findings.filter((f) => f.level === 'W').length;
    console.log(`\n${e} error(s), ${w} warning(s), ${r.pass.length} passed\n`);
  }
}

const errors = reports.flatMap((r) => r.findings).filter((f) => f.level === 'E').length;
const warns = reports.flatMap((r) => r.findings).filter((f) => f.level === 'W').length;
process.exit(errors || (flags.has('--strict') && warns) ? 1 : 0);
