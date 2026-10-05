const test = require('node:test');
const assert = require('node:assert/strict');
const childProcess = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { planUpgrade } = require('../src/cli/commands/upgrade');
const { listInstalledSkills } = require('../src/core/installed');
const { parseArgs: parseAuditArgs } = require('../src/audit/skill-overlap-report');
const { getAvailableSkills } = require('../src/core/skills');

const BIN = path.join(__dirname, '..', 'bin', 'nxa.js');
const [SKILL_A, SKILL_B] = getAvailableSkills();

/** Run the CLI in a throwaway project dir with a throwaway HOME. */
function sandbox() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'nxa-e2e-'));
  const cwd = path.join(root, 'project');
  const home = path.join(root, 'home');
  fs.mkdirSync(cwd);
  fs.mkdirSync(home);

  const run = (...args) => childProcess.spawnSync(process.execPath, [BIN, ...args], {
    cwd,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    env: { ...process.env, HOME: home, USERPROFILE: home }
  });

  return { root, cwd, home, run, cleanup: () => fs.rmSync(root, { recursive: true, force: true }) };
}

function entries(dir) {
  return fs.existsSync(dir) ? fs.readdirSync(dir).sort() : [];
}

test('install --help prints help and writes nothing', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const result = box.run('install', '--help');
  assert.equal(result.status, 0);
  assert.match(result.stdout, /Usage:/);
  assert.deepEqual(entries(box.cwd), []);
});

test('usage mistakes exit 2, print to stderr, and write nothing', t => {
  const box = sandbox();
  t.after(box.cleanup);

  for (const args of [['install', SKILL_A], ['install', '--globl'], ['bogus'], ['install', '--skill']]) {
    const result = box.run(...args);
    assert.equal(result.status, 2, args.join(' '));
    assert.match(result.stderr, /❌/);
    assert.equal(result.stdout, '');
  }
  assert.deepEqual(entries(box.cwd), []);
});

test('an unknown skill, plugin, or agent fails the whole install before writing', t => {
  const box = sandbox();
  t.after(box.cleanup);

  for (const args of [
    ['install', '--skill', `${SKILL_A},no-such-skill`],
    ['install', '--skill', SKILL_A, '--plugin', 'no-such-plugin'],
    ['install', '--skill', SKILL_A, '-a', 'no-such-agent']
  ]) {
    const result = box.run(...args);
    assert.equal(result.status, 1, args.join(' '));
    assert.match(result.stderr, /Unknown/);
  }
  assert.deepEqual(entries(box.cwd), []);
});

test('install writes only the selected skill, to the right scope', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const project = box.run('install', '--skill', SKILL_A);
  assert.equal(project.status, 0, project.stderr);
  assert.deepEqual(entries(path.join(box.cwd, '.agents', 'skills')), [SKILL_A]);

  const global = box.run('install', '--skill', SKILL_B, '--global');
  assert.equal(global.status, 0, global.stderr);
  assert.deepEqual(entries(path.join(box.home, '.agents', 'skills')), [SKILL_B]);
  assert.deepEqual(entries(path.join(box.cwd, '.agents', 'skills')), [SKILL_A]);
});

test('upgrade replaces only installed skills and leaves unknown ones alone', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const dir = path.join(box.home, '.agents', 'skills');
  assert.equal(box.run('install', '-g', '--skill', SKILL_A).status, 0);
  fs.writeFileSync(path.join(dir, SKILL_A, 'SKILL.md'), 'stale');
  fs.mkdirSync(path.join(dir, 'my-private-skill'));
  fs.writeFileSync(path.join(dir, 'my-private-skill', 'SKILL.md'), 'mine');

  const result = box.run('upgrade', '-g', '--overwrite');
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Left unchanged, not in .*my-private-skill/);
  assert.deepEqual(entries(dir), [SKILL_A, 'my-private-skill']);
  assert.notEqual(fs.readFileSync(path.join(dir, SKILL_A, 'SKILL.md'), 'utf8'), 'stale');
  assert.equal(fs.readFileSync(path.join(dir, 'my-private-skill', 'SKILL.md'), 'utf8'), 'mine');
});

test('upgrade and install --upgrade keep .env and .env.local and replace everything else', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const dir = path.join(box.home, '.agents', 'skills', SKILL_A);
  const write = (relative, content) => {
    fs.mkdirSync(path.dirname(path.join(dir, relative)), { recursive: true });
    fs.writeFileSync(path.join(dir, relative), content);
  };

  for (const args of [['upgrade', '-g', '--overwrite'], ['install', '-g', '-u', '-o', '--skill', SKILL_A]]) {
    assert.equal(box.run('install', '-g', '--skill', SKILL_A).status, 0);
    write('.env', 'SECRET=1');
    write('.env.local', 'LOCAL=1');
    write('scripts/.env', 'NESTED=1');
    write('scripts/.env.local', 'NESTED_LOCAL=1');
    write('.env.example', 'TEMPLATE=');
    write('.env.production', 'PROD=1');
    write('references/notes.md', 'local');
    write('output/run1/image.png', 'png');
    write('SKILL.md', 'stale');

    const result = box.run(...args);
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /kept .*\.env/);
    assert.equal(fs.readFileSync(path.join(dir, '.env'), 'utf8'), 'SECRET=1');
    assert.equal(fs.readFileSync(path.join(dir, '.env.local'), 'utf8'), 'LOCAL=1');
    assert.equal(fs.readFileSync(path.join(dir, 'scripts', '.env'), 'utf8'), 'NESTED=1');
    assert.equal(fs.readFileSync(path.join(dir, 'scripts', '.env.local'), 'utf8'), 'NESTED_LOCAL=1');
    assert.equal(fs.existsSync(path.join(dir, '.env.example')), false, '.env.example is not kept');
    assert.equal(fs.existsSync(path.join(dir, '.env.production')), false, 'other .env.* files are not kept');
    assert.equal(fs.existsSync(path.join(dir, 'references', 'notes.md')), false, 'local reference files are not kept');
    assert.equal(fs.existsSync(path.join(dir, 'output')), false, 'other local files are not kept');
    assert.notEqual(fs.readFileSync(path.join(dir, 'SKILL.md'), 'utf8'), 'stale');

    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('upgrade without --overwrite refuses to prompt when input is not a terminal', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const dir = path.join(box.home, '.agents', 'skills');
  assert.equal(box.run('install', '-g', '--skill', SKILL_A).status, 0);
  fs.writeFileSync(path.join(dir, SKILL_A, 'SKILL.md'), 'stale');

  const result = box.run('upgrade', '-g');
  assert.equal(result.status, 1);
  assert.match(result.stderr, /--overwrite/);
  assert.equal(fs.readFileSync(path.join(dir, SKILL_A, 'SKILL.md'), 'utf8'), 'stale');
});

test('upgrade --skill fails for a skill that is not installed', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const result = box.run('upgrade', '-g', '--overwrite', '--skill', SKILL_A);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Not installed/);
});

test('planUpgrade keeps to installed skills and the selection', () => {
  const targets = [{ dir: 'one', labels: ['One'] }, { dir: 'two', labels: ['Two'] }];
  const installed = new Map([['one', ['a', 'b', 'local']], ['two', ['b']]]);
  const all = planUpgrade(targets, installed, ['a', 'b', 'c'], { selected: false, explicit: [], skills: [] });

  assert.deepEqual(all.plan.map(t => t.skills), [['a', 'b'], ['b']]);
  assert.deepEqual(all.notInSource, ['local']);

  const some = planUpgrade(targets, installed, ['a', 'b', 'c'], { selected: true, explicit: ['b', 'c'], skills: ['b', 'c'] });
  assert.deepEqual(some.plan.map(t => t.skills), [['b'], ['b']]);
  assert.deepEqual(some.notInstalled, ['c']);
});

test('listInstalledSkills ignores folders without SKILL.md and hidden staging folders', t => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'nxa-installed-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  for (const name of ['real', '.real.nxa-staging-1', 'empty']) fs.mkdirSync(path.join(dir, name));
  fs.writeFileSync(path.join(dir, 'real', 'SKILL.md'), '');
  fs.writeFileSync(path.join(dir, '.real.nxa-staging-1', 'SKILL.md'), '');

  assert.deepEqual(listInstalledSkills(dir), ['real']);
  assert.deepEqual(listInstalledSkills(path.join(dir, 'missing')), []);
});

test('audit-overlap rejects bad options instead of ignoring them', () => {
  assert.throws(() => parseAuditArgs(['--threshold', 'abc']), /number from 0 to 1/);
  assert.throws(() => parseAuditArgs(['--top']), /needs a value/);
  assert.throws(() => parseAuditArgs(['--bogus']), /Unknown option/);
  assert.throws(() => parseAuditArgs(['--json-only', '--md-only']), /cannot be used together/);
  assert.equal(parseAuditArgs(['-t', '0.3', '--top', '5']).top, 5);
});

test('remove --yes keeps .env and .env.local in place and deletes everything else', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const dir = path.join(box.home, '.agents', 'skills');
  const skillDir = path.join(dir, SKILL_A);
  assert.equal(box.run('install', '-g', '--skill', `${SKILL_A},${SKILL_B}`).status, 0);
  fs.writeFileSync(path.join(skillDir, '.env'), 'SECRET=1');
  fs.mkdirSync(path.join(skillDir, 'scripts'), { recursive: true });
  fs.writeFileSync(path.join(skillDir, 'scripts', '.env.local'), 'LOCAL=1');
  fs.writeFileSync(path.join(skillDir, '.env.example'), 'TEMPLATE=');

  const result = box.run('remove', '-g', '-y', '--skill', SKILL_A);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /kept .*\.env/);
  assert.equal(fs.readFileSync(path.join(skillDir, '.env'), 'utf8'), 'SECRET=1');
  assert.equal(fs.readFileSync(path.join(skillDir, 'scripts', '.env.local'), 'utf8'), 'LOCAL=1');
  assert.deepEqual(entries(skillDir), ['.env', 'scripts']);
  assert.deepEqual(entries(path.join(skillDir, 'scripts')), ['.env.local']);
  assert.deepEqual(entries(dir), [SKILL_A, SKILL_B]);

  // The leftover folder is not an installed skill, so list and install treat it as absent.
  assert.deepEqual(box.run('list', '-i', '-g').stdout.trim().split('\n'), [SKILL_B]);
  const reinstall = box.run('install', '-g', '--skill', SKILL_A);
  assert.equal(reinstall.status, 0, reinstall.stderr);
  assert.match(reinstall.stdout, /✅/);
  assert.ok(fs.existsSync(path.join(skillDir, 'SKILL.md')));
  assert.equal(fs.readFileSync(path.join(skillDir, '.env'), 'utf8'), 'SECRET=1');
});

test('remove --delete-env deletes the whole folder; a skill with no .env goes entirely', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const dir = path.join(box.home, '.agents', 'skills');
  assert.equal(box.run('install', '-g', '--skill', `${SKILL_A},${SKILL_B}`).status, 0);
  fs.writeFileSync(path.join(dir, SKILL_A, '.env'), 'SECRET=1');

  const result = box.run('remove', '-g', '-y', '--delete-env', '--skill', `${SKILL_A},${SKILL_B}`);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /will be deleted/);
  assert.deepEqual(entries(dir), []);
});

test('remove refuses unknown names, missing selection, and silent prompts', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const dir = path.join(box.home, '.agents', 'skills');
  assert.equal(box.run('install', '-g', '--skill', SKILL_A).status, 0);

  const missing = box.run('remove', '-g', '-y', '--skill', `${SKILL_A},not-installed`);
  assert.equal(missing.status, 1);
  assert.match(missing.stderr, /Not installed.*not-installed.*Nothing was removed/s);

  assert.equal(box.run('remove', '-g', '-y').status, 2);

  const noTerminal = box.run('remove', '-g', '--skill', SKILL_A);
  assert.equal(noTerminal.status, 1);
  assert.match(noTerminal.stderr, /--overwrite/);

  assert.deepEqual(entries(dir), [SKILL_A]);
});

test('remove can delete a skill the source does not have', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const dir = path.join(box.home, '.agents', 'skills');
  fs.mkdirSync(path.join(dir, 'my-private-skill'), { recursive: true });
  fs.writeFileSync(path.join(dir, 'my-private-skill', 'SKILL.md'), 'mine');

  const result = box.run('remove', '-g', '--yes', '-s', 'my-private-skill');
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(entries(dir), []);
});

test('list --installed shows each target and flags skills without a source', t => {
  const box = sandbox();
  t.after(box.cleanup);

  const dir = path.join(box.home, '.agents', 'skills');
  assert.equal(box.run('install', '-g', '--skill', SKILL_A).status, 0);
  fs.mkdirSync(path.join(dir, 'my-private-skill'));
  fs.writeFileSync(path.join(dir, 'my-private-skill', 'SKILL.md'), '---\nname: my-private-skill\ndescription: Mine.\n---\n');
  fs.writeFileSync(path.join(dir, SKILL_A, '.env'), 'SECRET=1');

  const names = box.run('list', '--installed', '-g');
  assert.equal(names.status, 0, names.stderr);
  assert.deepEqual(names.stdout.trim().split('\n'), [SKILL_A, 'my-private-skill']);

  const full = box.run('list', '-i', '-g', '--full');
  assert.match(full.stdout, /my-private-skill {2}\[not in /);
  assert.match(full.stdout, new RegExp(`${SKILL_A} {2}\\[has \\.env\\]`));

  assert.equal(box.run('list', '-i', '-g', '-c').stdout.trim(), '2');
  assert.equal(box.run('list', '-i').stdout.trim(), '', 'project scope is empty');
});
