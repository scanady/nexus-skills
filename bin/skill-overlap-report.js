#!/usr/bin/env node
/**
 * skill-overlap-report.js
 *
 * Analyzes skills/ for duplicate and overlapping skills, produces a ranked
 * overlap report as JSON and Markdown.
 *
 * Usage (direct):
 *   node bin/skill-overlap-report.js [options]
 *
 * Usage (via CLI):
 *   node bin/cli.js audit-overlap [options]
 *
 * Options:
 *   --threshold, -t <n>   Minimum overall score to include (default: 0.20)
 *   --top <n>             Limit to top N pairs (default: all)
 *   --json-only           Only write JSON report
 *   --md-only             Only write Markdown report
 *   --output, -o <dir>    Output directory (default: output/)
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const { SKILLS_DIR, OUTPUT_DIR, getAvailableSkills } = require('./skills-core');

// ── Frontmatter parser ─────────────────────────────────────────────────────

function extractFrontmatterBlock(raw) {
  const lines = raw.split('\n');
  let start = -1, end = -1;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === '---') {
      if (start === -1) { start = i; }
      else              { end   = i; break; }
    }
  }
  if (start === -1 || end === -1) return { fm: '', bodyStart: 0 };
  return { fm: lines.slice(start + 1, end).join('\n'), bodyStart: end + 1 };
}

function extractTopField(fm, field) {
  const re = new RegExp('^' + field + ':\\s*(.*)$', 'm');
  const m  = fm.match(re);
  if (!m) return '';
  const v = m[1].trim().replace(/^["']/, '').replace(/["']\s*$/, '').trim();
  if (/^[>|][+-]?$/.test(v)) {
    const after = fm.slice(fm.indexOf(m[0]) + m[0].length);
    const lines = [];
    for (const ln of after.split('\n')) {
      if (/^\s+\S/.test(ln)) lines.push(ln.trim());
      else if (lines.length > 0) break;
    }
    return lines.join(' ');
  }
  return v;
}

function extractNestedField(fm, field) {
  const re = new RegExp('^\\s+' + field + ':\\s*(.*)$', 'm');
  const m  = fm.match(re);
  if (!m) return '';
  const v = m[1].trim().replace(/^["']/, '').replace(/["']\s*$/, '').trim();
  if (/^[>|][+-]?$/.test(v)) {
    const after = fm.slice(fm.indexOf(m[0]) + m[0].length);
    const lines = [];
    for (const ln of after.split('\n')) {
      if (/^\s{4,}\S/.test(ln)) lines.push(ln.trim());
      else if (lines.length > 0) break;
    }
    return lines.join(' ');
  }
  return v;
}

// ── Tokenizer ──────────────────────────────────────────────────────────────

// Generic grammatical noise only — domain words like "review", "audit",
// "analysis", "research", "design", "create", "generate", "scan" are kept
// because they carry strong routing signal.
const STOP_WORDS = new Set([
  'a','an','the','and','or','but','in','on','at','to','for','of','with','by',
  'from','as','is','was','are','were','be','been','have','has','had','do',
  'does','did','will','would','could','should','may','might','can','not','no',
  'use','using','when','where','what','which','who','how','also','all',
  'any','more','most','other','some','such','than','then','this','that','into',
  'about','after','before','if','while','per','user','users','needs','need',
  'want','wants','provide','provides','based','include','includes','including',
  'contains','contain','asked','ask','request','output','input',
  'help','helps','run','running','one','two','three',
  'get','set','make','new','its','your','our','you','i','me','my',
]);

function tokenize(text) {
  if (!text) return new Set();
  return new Set(
    text.toLowerCase()
      .replace(/[^\w\s-]/g, ' ')
      .split(/[\s,;|/\\]+/)
      .map(t => t.replace(/^-+|-+$/g, '').trim())
      .filter(t => t.length > 2 && !STOP_WORDS.has(t) && !/^\d+$/.test(t))
  );
}

// ── Similarity ─────────────────────────────────────────────────────────────

function jaccard(a, b) {
  if (!a.size && !b.size) return 0;
  let inter = 0;
  for (const x of a) if (b.has(x)) inter++;
  return inter / (a.size + b.size - inter);
}

function nameSegmentSim(nameA, nameB) {
  const sa = new Set(nameA.split('-').filter(s => s.length > 1));
  const sb = new Set(nameB.split('-').filter(s => s.length > 1));
  return jaccard(sa, sb);
}

function metadataSim(a, b) {
  const fields = ['domain', 'scope', 'outputFormat'];
  let matches = 0, total = 0;
  for (const f of fields) {
    if (a[f] || b[f]) {
      total++;
      if (a[f] && b[f] && a[f].toLowerCase() === b[f].toLowerCase()) matches++;
    }
  }
  return total > 0 ? matches / total : 0;
}

// Scoring weights
const WEIGHTS = { trigger: 0.35, desc: 0.25, body: 0.15, name: 0.15, meta: 0.10 };

function computeScores(a, b) {
  const trigger = jaccard(a.triggerTokens, b.triggerTokens);
  const desc    = jaccard(a.descTokens,    b.descTokens);
  const body    = jaccard(a.bodyTokens,    b.bodyTokens);
  const name    = nameSegmentSim(a.name,   b.name);
  const meta    = metadataSim(a, b);
  const overall = r2(
    trigger * WEIGHTS.trigger +
    desc    * WEIGHTS.desc    +
    body    * WEIGHTS.body    +
    name    * WEIGHTS.name    +
    meta    * WEIGHTS.meta
  );
  const shared = [...a.triggerTokens].filter(t => b.triggerTokens.has(t)).slice(0, 12);
  return { overall, trigger: r2(trigger), desc: r2(desc), body: r2(body), name: r2(name), meta: r2(meta), shared };
}

function r2(n) { return Math.round(n * 100) / 100; }

// ── Overlap classification ─────────────────────────────────────────────────

/**
 * Overlap types (highest to lowest severity):
 *
 * duplicate               — strong merge/archive signal; same user intent + output
 * merge-candidate         — same domain+category with meaningful functional overlap
 * template-twin           — descriptions nearly identical (copy-paste template)
 * routing-collision       — competing trigger phrases; needs boundary work
 * umbrella-plus-specialist — one broad, one narrow within shared name prefix
 * adjacent-distinct       — related vocabulary, clearly different purpose
 */
function classify(a, b, s) {
  const pa = a.name.split('-');
  const pb = b.name.split('-');
  const sharedPrefixLen = pa.filter((seg, i) => pb[i] === seg).length;

  // Template-twin: description token overlap >= 0.60 regardless of trigger overlap.
  // Catches copy-pasted skill shells ("Creates viral X posts..." / "Creates viral LinkedIn posts...").
  if (s.desc >= 0.60) return 'template-twin';

  // Duplicate: high combined score OR strong trigger overlap with similar names
  if (s.overall >= 0.35) return 'duplicate';
  if (s.trigger >= 0.28 && s.name >= 0.50) return 'duplicate';

  // Merge-candidate: same domain+category prefix AND meaningful signal on both axes
  if (sharedPrefixLen >= 2 && s.overall >= 0.22 && s.trigger >= 0.18) return 'merge-candidate';
  // Very similar names with moderate overall (e.g. tech-security-reviewer vs tech-security-analyst)
  if (s.name >= 0.70 && s.overall >= 0.20) return 'merge-candidate';

  // Routing collision: competing trigger phrases without strong structural match
  if (s.trigger >= 0.22 && s.overall >= 0.22) return 'routing-collision';

  // Umbrella/specialist: shared prefix, but one is significantly broader (by trigger count)
  if (sharedPrefixLen >= 2 && s.overall >= 0.16) {
    const trigSizes = [a.triggerTokens.size, b.triggerTokens.size];
    const ratio = Math.max(...trigSizes) / Math.max(Math.min(...trigSizes), 1);
    if (ratio >= 1.6) return 'umbrella-plus-specialist';
    return 'routing-collision';
  }

  return 'adjacent-distinct';
}

const RECOMMENDATIONS = {
  'duplicate':
    'Strong merge or archive candidate — same user intent and output artifact detected. Consolidate into one skill and move the other to skills-sandbox/.',
  'merge-candidate':
    'Review for consolidation — same domain+category with significant functional overlap. Confirm whether unique knowledge justifies two separate skills.',
  'template-twin':
    'Descriptions are near-identical (likely copy-pasted). Differentiate with platform/domain-specific content, or merge if the use cases overlap.',
  'routing-collision':
    'Sharpen description and trigger boundaries; add anti-trigger notes or update related-skills links.',
  'umbrella-plus-specialist':
    'Verify the broader skill explicitly defers to the specialist; add related-skills cross-links.',
  'adjacent-distinct':
    'Low risk — verify trigger phrases do not collide in practice.',
};

const TYPE_ORDER = ['duplicate', 'merge-candidate', 'template-twin', 'routing-collision', 'umbrella-plus-specialist', 'adjacent-distinct'];

// ── Skill loader ───────────────────────────────────────────────────────────

function loadSkill(name) {
  const skillFile = path.join(SKILLS_DIR, name, 'SKILL.md');
  let raw;
  try { raw = fs.readFileSync(skillFile, 'utf8'); } catch { return null; }

  const { fm, bodyStart } = extractFrontmatterBlock(raw);
  const bodyLines = raw.split('\n').slice(bodyStart, bodyStart + 80).join('\n');

  const description  = extractTopField(fm,    'description');
  const triggers     = extractNestedField(fm,  'triggers');
  const role         = extractNestedField(fm,  'role');
  const domain       = extractNestedField(fm,  'domain');
  const scope        = extractNestedField(fm,  'scope');
  const outputFormat = extractNestedField(fm,  'output-format') ||
                       extractNestedField(fm,  'output_format');

  return {
    name,
    description,
    triggers,
    domain,
    scope,
    outputFormat,
    // Include role tokens — they're discriminating signals (e.g. "analyst" vs "reviewer")
    triggerTokens: tokenize(`${triggers} ${role}`),
    descTokens:    tokenize(description),
    bodyTokens:    tokenize(bodyLines),
  };
}

// ── Clustering ─────────────────────────────────────────────────────────────

function clusterPairs(pairs) {
  const clusters = [];
  for (const p of pairs) {
    const found = clusters.find(c =>
      c.skills.includes(p.skillA) || c.skills.includes(p.skillB)
    );
    if (found) {
      if (!found.skills.includes(p.skillA)) found.skills.push(p.skillA);
      if (!found.skills.includes(p.skillB)) found.skills.push(p.skillB);
      found.pairs.push(p);
      if (p.overall > found.maxScore) found.maxScore = p.overall;
    } else {
      clusters.push({
        id:       `cluster-${clusters.length + 1}`,
        skills:   [p.skillA, p.skillB],
        pairs:    [p],
        maxScore: p.overall,
      });
    }
  }
  return clusters.sort((a, b) => b.maxScore - a.maxScore);
}

// ── Markdown report ────────────────────────────────────────────────────────

function buildMarkdown(pairs, clusters, skillCount, threshold, now) {
  const L = [];
  const typeCounts = {};
  for (const p of pairs) typeCounts[p.overlapType] = (typeCounts[p.overlapType] || 0) + 1;

  L.push('# Skill Catalog Overlap Report', '');
  L.push(`Generated: ${now}  `);
  L.push(`Skills scanned: ${skillCount}  `);
  L.push(`Pairs at threshold ≥ ${threshold}: ${pairs.length}  `);
  L.push(`Clusters identified: ${clusters.length}`, '');

  L.push('## Summary', '');
  L.push('| Overlap Type | Pairs | Action |');
  L.push('|---|---|---|');
  const typeActions = {
    'duplicate':                'Merge or archive ⚠️',
    'merge-candidate':          'Review for consolidation ⚠️',
    'template-twin':            'Differentiate descriptions or merge',
    'routing-collision':        'Sharpen triggers/descriptions',
    'umbrella-plus-specialist': 'Add routing links',
    'adjacent-distinct':        'Monitor / no action',
  };
  for (const t of TYPE_ORDER) {
    if (typeCounts[t]) {
      L.push(`| \`${t}\` | ${typeCounts[t]} | ${typeActions[t]} |`);
    }
  }
  L.push('');

  const actionItems = pairs
    .filter(p => ['duplicate', 'merge-candidate', 'template-twin', 'routing-collision'].includes(p.overlapType))
    .slice(0, 20);
  if (actionItems.length) {
    L.push('## Action Items', '');
    L.push('Pairs requiring attention, ranked by severity then score:', '');
    L.push('| # | Skill A | Skill B | Type | Score |');
    L.push('|---|---|---|---|---|');
    actionItems.forEach((p, i) => {
      L.push(`| ${i + 1} | \`${p.skillA}\` | \`${p.skillB}\` | \`${p.overlapType}\` | ${p.overall} |`);
    });
    L.push('');
  }

  L.push('## Clusters', '');
  for (const c of clusters) {
    const sortedPairs = [...c.pairs].sort((a, b) => {
      const ta = TYPE_ORDER.indexOf(a.overlapType);
      const tb = TYPE_ORDER.indexOf(b.overlapType);
      if (ta !== tb) return ta - tb;
      return b.overall - a.overall;
    });
    const topType = sortedPairs[0].overlapType;
    L.push(`### ${c.id} — \`${topType}\` (max score: ${c.maxScore})`, '');
    L.push(`**Skills:** ${c.skills.map(s => `\`${s}\``).join(', ')}`, '');
    L.push('| Pair | Score | Trigger | Desc | Name |');
    L.push('|---|---|---|---|---|');
    for (const p of sortedPairs) {
      L.push(`| \`${p.skillA}\` ↔ \`${p.skillB}\` | ${p.overall} | ${p.trigger} | ${p.desc} | ${p.name} |`);
    }
    L.push('');
    const top = sortedPairs[0];
    if (top.shared.length) {
      L.push(`**Shared trigger tokens:** ${top.shared.map(t => `\`${t}\``).join(', ')}`, '');
    }
    L.push(`**Recommendation:** ${RECOMMENDATIONS[topType] || ''}`, '');
  }

  L.push('## All Pairs', '');
  L.push('| Skill A | Skill B | Type | Score | Trigger | Desc | Name |');
  L.push('|---|---|---|---|---|---|---|');
  for (const p of pairs) {
    L.push(`| \`${p.skillA}\` | \`${p.skillB}\` | \`${p.overlapType}\` | ${p.overall} | ${p.trigger} | ${p.desc} | ${p.name} |`);
  }
  L.push('');
  L.push('---');
  L.push('*Generated by `node bin/skill-overlap-report.js`. Rerun after any catalog change.*');
  return L.join('\n');
}

// ── Arg parser ─────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const opts = { threshold: 0.20, top: null, jsonOnly: false, mdOnly: false, outputDir: OUTPUT_DIR };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if ((a === '--threshold' || a === '-t') && argv[i + 1]) opts.threshold = parseFloat(argv[++i]);
    else if (a === '--top' && argv[i + 1])                  opts.top = parseInt(argv[++i], 10);
    else if (a === '--json-only')                            opts.jsonOnly = true;
    else if (a === '--md-only')                              opts.mdOnly = true;
    else if ((a === '--output' || a === '-o') && argv[i + 1]) opts.outputDir = argv[++i];
  }
  return opts;
}

// ── Main ───────────────────────────────────────────────────────────────────

function run(argv) {
  const { threshold, top, jsonOnly, mdOnly, outputDir } = parseArgs(argv || []);

  console.log('\n🔍 Scanning skills/ for overlap...\n');

  const names  = getAvailableSkills();
  const skills = names.map(loadSkill).filter(Boolean);
  console.log(`   Found ${skills.length} skills`);

  if (skills.length < 2) {
    console.log('   Not enough skills to compare.\n');
    return;
  }

  const pairs = [];
  for (let i = 0; i < skills.length; i++) {
    for (let j = i + 1; j < skills.length; j++) {
      const s = computeScores(skills[i], skills[j]);
      if (s.overall < threshold) continue;
      const overlapType = classify(skills[i], skills[j], s);
      pairs.push({ skillA: skills[i].name, skillB: skills[j].name, overlapType, ...s });
    }
  }

  // Sort by type severity first, then score descending
  pairs.sort((a, b) => {
    const ta = TYPE_ORDER.indexOf(a.overlapType);
    const tb = TYPE_ORDER.indexOf(b.overlapType);
    if (ta !== tb) return ta - tb;
    return b.overall - a.overall;
  });
  const reportPairs = top ? pairs.slice(0, top) : pairs;
  const clusters    = clusterPairs(reportPairs);

  const typeCounts = {};
  for (const p of reportPairs) typeCounts[p.overlapType] = (typeCounts[p.overlapType] || 0) + 1;

  console.log(`   Pairs ≥ ${threshold}: ${reportPairs.length}`);
  console.log(`   Clusters: ${clusters.length}`);
  for (const t of TYPE_ORDER) {
    if (typeCounts[t]) console.log(`   ${t}: ${typeCounts[t]}`);
  }

  const now = new Date().toISOString();
  const jsonOut = {
    generated_at: now,
    total_skills: skills.length,
    threshold,
    summary: {
      pairs_above_threshold: reportPairs.length,
      clusters: clusters.length,
      by_type:  typeCounts,
    },
    clusters: clusters.map(c => ({
      id:               c.id,
      max_score:        c.maxScore,
      skills:           c.skills,
      top_overlap_type: [...c.pairs].sort((a, b) => b.overall - a.overall)[0].overlapType,
      pairs: c.pairs.map(p => ({
        skill_a:         p.skillA,
        skill_b:         p.skillB,
        overlap_type:    p.overlapType,
        overall:         p.overall,
        trigger_jaccard: p.trigger,
        desc_jaccard:    p.desc,
        name_similarity: p.name,
        shared_triggers: p.shared,
        recommendation:  RECOMMENDATIONS[p.overlapType] || '',
      })),
    })),
    all_pairs: reportPairs.map(p => ({
      skill_a:             p.skillA,
      skill_b:             p.skillB,
      overlap_type:        p.overlapType,
      overall:             p.overall,
      trigger_jaccard:     p.trigger,
      desc_jaccard:        p.desc,
      name_similarity:     p.name,
      metadata_similarity: p.meta,
      shared_triggers:     p.shared,
      recommendation:      RECOMMENDATIONS[p.overlapType] || '',
    })),
  };

  fs.mkdirSync(outputDir, { recursive: true });

  if (!mdOnly) {
    const jp = path.join(outputDir, 'skill-overlap-report.json');
    fs.writeFileSync(jp, JSON.stringify(jsonOut, null, 2));
    console.log(`\n✅ JSON     → ${jp}`);
  }
  if (!jsonOnly) {
    const mp = path.join(outputDir, 'skill-overlap-report.md');
    fs.writeFileSync(mp, buildMarkdown(reportPairs, clusters, skills.length, threshold, now));
    console.log(`✅ Markdown → ${mp}`);
  }

  // Print all action-required items to console
  const actionItems = reportPairs.filter(p =>
    ['duplicate', 'merge-candidate', 'template-twin', 'routing-collision'].includes(p.overlapType)
  );
  if (actionItems.length) {
    console.log('\n⚠️  Action items:\n');
    actionItems.forEach((p, i) => {
      console.log(`   ${i + 1}. [${p.overlapType}] ${p.skillA} ↔ ${p.skillB} (score: ${p.overall})`);
      if (p.shared.length) {
        console.log(`      shared: ${p.shared.slice(0, 6).join(', ')}`);
      }
    });
  }

  console.log('');
}

if (require.main === module) {
  run(process.argv.slice(2));
}

module.exports = { run };
