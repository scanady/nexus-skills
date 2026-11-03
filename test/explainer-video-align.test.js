const test = require('node:test');
const assert = require('node:assert/strict');

const load = () => import('../skills/design-visual-explainer-video/scripts/lib/align.mjs');
// Fake Whisper output: one word every 0.5 s.
const heardFrom = text => text.split(' ').map((t, i) => ({ text: t, start: i * 0.5, end: i * 0.5 + 0.4 }));

test('spokenTokens expands numbers, money, years, and domains', async () => {
  const { spokenTokens } = await load();
  assert.deepEqual(spokenTokens('40%,'), ['forty', 'percent']);
  assert.deepEqual(spokenTokens('$1,050.'), ['one', 'thousand', 'fifty', 'dollars']);
  assert.deepEqual(spokenTokens('1582'), ['fifteen', 'eighty', 'two']);
  assert.deepEqual(spokenTokens('1900'), ['nineteen', 'hundred']);
  assert.deepEqual(spokenTokens('2005'), ['two', 'thousand', 'five']);
  assert.deepEqual(spokenTokens('example.com'), ['example', 'dot', 'com']);
  assert.deepEqual(spokenTokens("It's"), ['its']);
});

test('alignWords gives measured times when every word is heard', async () => {
  const { alignWords } = await load();
  const words = 'the sky is blue'.split(' ');
  const r = alignWords(words, heardFrom('The sky is blue.'), 2);
  assert.equal(r.matchRate, 1);
  assert.deepEqual(r.words.map(w => w.t), [0, 0.5, 1, 1.5]);
  assert.ok(r.words.every(w => w.heard));
});

test('alignWords reports a wrong word and spreads its time between neighbours', async () => {
  const { alignWords } = await load();
  const r = alignWords('the sky is blue'.split(' '), heardFrom('the sky was blue'), 2);
  assert.equal(r.words[2].heard, false);
  assert.ok(r.words[2].t >= r.words[1].end && r.words[2].t <= r.words[3].t);
  assert.equal(r.matchRate, 0.75);
});

test('alignWords matches digits to spelled-out numbers and joins split numbers', async () => {
  const { alignWords } = await load();
  assert.equal(alignWords(['forty', 'percent'], heardFrom('40%'), 1).matchRate, 1);
  const split = [{ text: '$1', start: 0, end: 0.2 }, { text: ',000', start: 0.2, end: 0.4 }];
  assert.equal(alignWords('one thousand dollars'.split(' '), split, 1).matchRate, 1);
  assert.equal(alignWords('one thousand and fifty dollars'.split(' '), heardFrom('$1,050'), 1).matchRate, 1);
});

test('alignWords accepts one word heard as two, and a close spelling', async () => {
  const { alignWords } = await load();
  assert.equal(alignWords(['database'], heardFrom('data base'), 1).matchRate, 1);
  assert.equal(alignWords(['data', 'base'], heardFrom('database'), 1).matchRate, 1);
  assert.equal(alignWords(['Friender'], heardFrom('Friendr'), 1).matchRate, 1);
});

test('alignWords reports silence as nothing heard, with times inside the clip', async () => {
  const { alignWords } = await load();
  const r = alignWords(['one', 'two'], [], 2);
  assert.equal(r.matchRate, 0);
  assert.ok(r.words.every(w => !w.heard && w.t >= 0 && w.end <= 2));
});

test('timesForText maps spoken times back to the caption words', async () => {
  const { timesForText } = await load();
  // say: "about forty percent of Friender dot N L users"
  const timed = 'about forty percent of Friender dot N L users'.split(' ').map((w, i) => ({ w, t: i, end: i + 0.5 }));
  const out = timesForText('about 40 percent of Friendr.nl users', timed);
  assert.deepEqual(out.map(w => w.w), ['about', '40', 'percent', 'of', 'Friendr.nl', 'users']);
  assert.deepEqual(out.map(w => w.t), [0, 1, 2, 3, 4, 8]);
});

test('timesForText returns one time per caption word when nothing is shared', async () => {
  const { timesForText } = await load();
  const timed = [{ w: 'hello', t: 1, end: 1.4 }, { w: 'there', t: 2, end: 2.4 }];
  const out = timesForText('goodbye now friend', timed);
  assert.equal(out.length, 3);
  assert.ok(out.every(w => w.t >= 1 && w.t <= 2.4));
});

test('canCheckSpeech rejects languages written without spaces', async () => {
  const { canCheckSpeech } = await load();
  assert.equal(canCheckSpeech('en'), true);
  assert.equal(canCheckSpeech('nl'), true);
  assert.equal(canCheckSpeech('ja'), false);
  assert.equal(canCheckSpeech('zh-CN'), false);
});

const plan = () => import('../skills/design-visual-explainer-video/scripts/lib/plan.mjs');
const planScene = (over = {}) => ({ name: 'a', a0: 0, b0: 10, onScreen: ['The hook'], ...over });

test('contentNotes is quiet on a sound plan', async () => {
  const { contentNotes } = await plan();
  const lines = [{ text: 'It costs $1,050 and 40% less.' }];
  assert.deepEqual(contentNotes({ lines, scenes: [planScene()], facts: '- Costs 1,050, 40% less — https://example.org/2024' }), []);
});

test('contentNotes flags a missing hook, long text, and too little reading time', async () => {
  const { contentNotes } = await plan();
  const noHook = contentNotes({ lines: [], scenes: [planScene({ onScreen: [] })] });
  assert.match(noHook.join(), /no onScreen text/);
  const long = contentNotes({ lines: [], scenes: [planScene({ onScreen: ['one two three four five six seven eight nine'] })] });
  assert.match(long.join(), /has 9 words/);
  const short = contentNotes({ lines: [], scenes: [planScene({ b0: 2, onScreen: ['one two three four five six'] })] });
  assert.match(short.join(), /need at least 3\.0 s/);
});

test('contentNotes flags a number with no source and ignores digits in source URLs', async () => {
  const { contentNotes } = await plan();
  const notes = contentNotes({ lines: [{ text: 'Founded in 2024, with 15 staff.' }], scenes: [planScene()], facts: '- Has 15 staff — https://example.org/2024', userFacts: [] });
  assert.equal(notes.length, 1);
  assert.match(notes[0], /number 2024/);
  assert.deepEqual(contentNotes({ lines: [{ text: 'Founded in 2024.' }], scenes: [planScene()], userFacts: ['Founded in 2024 (chat)'] }), []);
});

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const scripts = path.join(__dirname, '../skills/design-visual-explainer-video/scripts');
const run = (script, args, cwd) => spawnSync(process.execPath, [path.join(scripts, script), ...args], { cwd, encoding: 'utf8' });
const tempDir = () => fs.mkdtempSync(path.join(os.tmpdir(), 'explainer-'));

test('init needs a full path and writes nothing without one', () => {
  const cwd = tempDir();
  for (const place of ['.', 'videos', '~/videos']) {
    const r = run('init.mjs', ['--in', place, '--name', 'a'], cwd);
    assert.notEqual(r.status, 0);
    assert.match(r.stderr, /must be a full path/);
  }
  assert.notEqual(run('init.mjs', ['--name', 'a'], cwd).status, 0);
  assert.deepEqual(fs.readdirSync(cwd), []);
});

test('init ignores EXPLAINER_OUTPUT_DIR and refuses the skill folder', () => {
  const cwd = tempDir();
  const env = { ...process.env, EXPLAINER_OUTPUT_DIR: cwd };
  const r = spawnSync(process.execPath, [path.join(scripts, 'init.mjs'), '--name', 'a'], { cwd, env, encoding: 'utf8' });
  assert.notEqual(r.status, 0);
  assert.deepEqual(fs.readdirSync(cwd), []);
  assert.match(run('init.mjs', ['--in', scripts, '--name', 'a'], cwd).stderr, /inside this skill/);
});

test('scripts stop outside a job folder and run inside one', () => {
  const parent = tempDir();
  assert.equal(run('init.mjs', ['--in', parent, '--name', 'a'], parent).status, 0);
  const job = path.join(parent, 'a', 'video', 'work');
  const outside = tempDir();
  const r = run('timeline.mjs', [], outside);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /not a job folder/);
  assert.deepEqual(fs.readdirSync(outside), []);
  // A folder named work with no project is not a job folder.
  const work = path.join(outside, 'work');
  fs.mkdirSync(work);
  assert.match(run('timeline.mjs', [], work).stderr, /not a job folder/);
  assert.doesNotMatch(run('timeline.mjs', [], job).stderr, /not a job folder/);
});
