const fs = require('fs');
const https = require('https');
const path = require('path');

const REPO_OWNER = process.env.FORGE_AGENTS_REPO_OWNER || 'scanady';
const REPO_NAME = process.env.FORGE_AGENTS_REPO_NAME || 'forge-agents';
const REPO_REF = process.env.FORGE_AGENTS_REPO_REF || 'main';
const SKILLS_PATH = 'skills';

function httpsGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'User-Agent': 'forge-agents-cli',
        'Accept': 'application/vnd.github+json'
      }
    }, (response) => {
      if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        response.resume();
        httpsGet(response.headers.location).then(resolve, reject);
        return;
      }

      if (response.statusCode !== 200) {
        response.resume();
        reject(new Error(`HTTP ${response.statusCode} for ${url}`));
        return;
      }

      const chunks = [];
      response.on('data', chunk => chunks.push(chunk));
      response.on('end', () => resolve(Buffer.concat(chunks)));
      response.on('error', reject);
    }).on('error', reject);
  });
}

async function fetchJSON(url) {
  const payload = await httpsGet(url);
  return JSON.parse(payload.toString('utf8'));
}

async function fetchText(url) {
  const payload = await httpsGet(url);
  return payload.toString('utf8');
}

async function fetchRemoteSkillList() {
  const url = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${SKILLS_PATH}?ref=${REPO_REF}`;
  const entries = await fetchJSON(url);
  return entries
    .filter(entry => entry.type === 'dir')
    .map(entry => entry.name)
    .sort((left, right) => left.localeCompare(right));
}

async function fetchRemoteSkillFrontmatter(skillName) {
  const url = `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${REPO_REF}/${SKILLS_PATH}/${skillName}/SKILL.md`;
  return fetchText(url);
}

async function listRemoteSkillFiles(skillName, apiUrl, relativePrefix = '') {
  const url = apiUrl || `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${SKILLS_PATH}/${skillName}?ref=${REPO_REF}`;
  const entries = await fetchJSON(url);
  const files = [];

  for (const entry of entries) {
    const relativePath = relativePrefix ? `${relativePrefix}/${entry.name}` : entry.name;

    if (entry.type === 'file') {
      files.push({
        path: relativePath,
        downloadUrl: entry.download_url
      });
      continue;
    }

    if (entry.type === 'dir') {
      const nestedFiles = await listRemoteSkillFiles(skillName, entry.url, relativePath);
      files.push(...nestedFiles);
    }
  }

  return files;
}

async function downloadRemoteSkill(skillName, destinationDir) {
  const files = await listRemoteSkillFiles(skillName);

  for (const file of files) {
    const destinationPath = path.join(destinationDir, file.path);
    fs.mkdirSync(path.dirname(destinationPath), { recursive: true });
    const content = await httpsGet(file.downloadUrl);
    fs.writeFileSync(destinationPath, content);
  }
}

module.exports = {
  downloadRemoteSkill,
  fetchRemoteSkillFrontmatter,
  fetchRemoteSkillList
};