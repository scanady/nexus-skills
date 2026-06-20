const childProcess = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const {
  SKILLS_DIR,
  extractFrontmatter,
  getAvailableSkills,
  isLocalMode,
  parseFrontmatter
} = require('./skills-core');
const {
  downloadRemoteSkill,
  fetchRemoteSkillFrontmatter,
  fetchRemoteSkillList
} = require('./github-fetch');
const { copyDir } = require('./file-system');

function getEnvValue(...names) {
  for (const name of names) {
    const value = process.env[name];
    if (value && value.trim()) {
      return value.trim();
    }
  }

  return '';
}

function getSkillsFromDir(skillsDir) {
  try {
    return fs.readdirSync(skillsDir)
      .filter(name => {
        const skillPath = path.join(skillsDir, name);
        return fs.statSync(skillPath).isDirectory() &&
          fs.existsSync(path.join(skillPath, 'SKILL.md'));
      })
      .sort((left, right) => left.localeCompare(right));
  } catch (error) {
    return [];
  }
}

function cloneRepoToTempDir(repoUrl, ref) {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-skills-'));
  const args = ['clone', '--depth', '1'];

  if (ref) {
    args.push('--branch', ref);
  }

  args.push(repoUrl, tempDir);

  const result = childProcess.spawnSync('git', args, {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe']
  });

  if (result.error) {
    fs.rmSync(tempDir, { recursive: true, force: true });
    throw new Error(`Failed to run git clone for ${repoUrl}: ${result.error.message}`);
  }

  if (result.status !== 0) {
    fs.rmSync(tempDir, { recursive: true, force: true });
    const stderr = (result.stderr || '').trim();
    throw new Error(stderr || `git clone failed for ${repoUrl}`);
  }

  return tempDir;
}

async function withClonedRepo(sourceConfig, work) {
  const repoDir = cloneRepoToTempDir(sourceConfig.repoUrl, sourceConfig.sourceRef);

  try {
    const skillsDir = path.join(repoDir, 'skills');
    if (!fs.existsSync(skillsDir) || !fs.statSync(skillsDir).isDirectory()) {
      throw new Error(`Repository ${sourceConfig.repoUrl} does not contain a skills/ directory.`);
    }

    return await work(skillsDir);
  } finally {
    fs.rmSync(repoDir, { recursive: true, force: true });
  }
}

function resolveSourceConfig(options = {}) {
  return {
    repoUrl: options.sourceUrl || getEnvValue('NYLD_NEXUS_SKILLS_SOURCE_URL', 'NEXUS_AGENTS_REPO_URL'),
    sourceRef: options.sourceRef || getEnvValue('NYLD_NEXUS_SKILLS_SOURCE_REF', 'NEXUS_AGENTS_REPO_REF')
  };
}

async function withSkillSource(options = {}, work) {
  const sourceConfig = resolveSourceConfig(options);

  if (sourceConfig.repoUrl) {
    return withClonedRepo(sourceConfig, skillsDir => work({
      type: 'repo',
      label: `repository ${sourceConfig.repoUrl}${sourceConfig.sourceRef ? `#${sourceConfig.sourceRef}` : ''}`,
      listSkills: () => getSkillsFromDir(skillsDir),
      getMetadata: skill => extractFrontmatter(path.join(skillsDir, skill, 'SKILL.md')),
      installSkill: (skill, destinationDir) => copyDir(path.join(skillsDir, skill), destinationDir)
    }));
  }

  if (isLocalMode()) {
    return work({
      type: 'local',
      label: 'local bundle',
      listSkills: () => getAvailableSkills(),
      getMetadata: skill => extractFrontmatter(path.join(SKILLS_DIR, skill, 'SKILL.md')),
      installSkill: (skill, destinationDir) => copyDir(path.join(SKILLS_DIR, skill), destinationDir)
    });
  }

  return work({
    type: 'github',
    label: 'GitHub fallback',
    listSkills: () => fetchRemoteSkillList(),
    getMetadata: async skill => parseFrontmatter(await fetchRemoteSkillFrontmatter(skill)),
    installSkill: (skill, destinationDir) => downloadRemoteSkill(skill, destinationDir)
  });
}

async function getSkillList() {
  return withSkillSource({}, source => source.listSkills());
}

async function getSkillMetadata(skill) {
  return withSkillSource({}, source => source.getMetadata(skill));
}

async function installSkill(skill, destinationDir) {
  return withSkillSource({}, source => source.installSkill(skill, destinationDir));
}

function getSourceLabel() {
  return isLocalMode() ? 'local bundle' : 'GitHub fallback';
}

module.exports = {
  getSkillList,
  getSkillMetadata,
  getSourceLabel,
  installSkill,
  resolveSourceConfig,
  withSkillSource
};
