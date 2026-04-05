const fs = require('fs');
const os = require('os');
const path = require('path');

const PROJECT_ROOT = path.join(__dirname, '..');
const SKILLS_DIR = path.join(PROJECT_ROOT, 'skills');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'output');

const AGENTS = {
    'agent-skills': {
        name: 'Agent Skills',
        aliases: ['agents', 'agentskills', 'standard'],
        projectDir: '.agents/skills',
        globalDir: path.join(os.homedir(), '.agents', 'skills')
    },
    'claude-code': {
        name: 'Claude Code',
        aliases: ['claude'],
        projectDir: '.claude/skills',
        globalDir: path.join(os.homedir(), '.claude', 'skills')
    },
    'github-copilot': {
        name: 'GitHub Copilot',
        aliases: ['copilot'],
        projectDir: '.agents/skills',
        globalDir: path.join(os.homedir(), '.copilot', 'skills')
    },
    'codex': {
        name: 'OpenAI Codex',
        aliases: ['openai-codex'],
        projectDir: '.agents/skills',
        globalDir: path.join(os.homedir(), '.codex', 'skills')
    }
};

const DEFAULT_AGENT = 'agent-skills';
const SKILL_NAME_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

function stripWrappingQuotes(value) {
    if (!value) {
        return '';
    }

    const trimmed = value.trim();
    if ((trimmed.startsWith('"') && trimmed.endsWith('"')) || (trimmed.startsWith("'") && trimmed.endsWith("'"))) {
        return trimmed.slice(1, -1).trim();
    }

    return trimmed;
}

function parseFrontmatter(content) {
    const lines = content.split('\n');
    const metadata = {};
    let inFrontmatter = false;

    for (const line of lines) {
        if (line.trim() === '---') {
            if (inFrontmatter) {
                break;
            }

            inFrontmatter = true;
            continue;
        }

        if (!inFrontmatter) {
            continue;
        }

        const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
        if (!match) {
            continue;
        }

        metadata[match[1]] = stripWrappingQuotes(match[2]);
    }

    return metadata;
}

function extractFrontmatter(filePath) {
    try {
        return parseFrontmatter(fs.readFileSync(filePath, 'utf8'));
    } catch (error) {
        return {};
    }
}

function getAvailableSkills() {
    try {
        return fs.readdirSync(SKILLS_DIR)
            .filter(name => {
                const skillPath = path.join(SKILLS_DIR, name);
                return fs.statSync(skillPath).isDirectory() &&
                    fs.existsSync(path.join(skillPath, 'SKILL.md'));
            })
            .sort((left, right) => left.localeCompare(right));
    } catch (error) {
        return [];
    }
}

function getSkillRecord(skillName) {
    const skillPath = path.join(SKILLS_DIR, skillName);
    const skillFile = path.join(skillPath, 'SKILL.md');
    const metadata = fs.existsSync(skillFile) ? extractFrontmatter(skillFile) : {};

    return {
        name: skillName,
        path: skillPath,
        skillFile,
        metadata
    };
}

function validateSkillStructure(skillPath) {
    const folderName = path.basename(skillPath);
    const skillFile = path.join(skillPath, 'SKILL.md');
    const errors = [];
    const warnings = [];

    if (!SKILL_NAME_PATTERN.test(folderName) || folderName.length > 64) {
        errors.push('Skill folder name must match the Agent Skills naming rules (lowercase letters, numbers, single hyphens, max 64 chars).');
    }

    if (!fs.existsSync(skillFile)) {
        errors.push('Missing SKILL.md.');
        return { errors, warnings, metadata: {} };
    }

    const metadata = extractFrontmatter(skillFile);
    if (!metadata.name) {
        errors.push('SKILL.md frontmatter is missing the required name field.');
    } else {
        if (metadata.name !== folderName) {
            errors.push(`SKILL.md name must match the folder name (${folderName}).`);
        }

        if (!SKILL_NAME_PATTERN.test(metadata.name) || metadata.name.length > 64) {
            errors.push('SKILL.md name does not satisfy the Agent Skills naming rules.');
        }
    }

    if (!metadata.description) {
        errors.push('SKILL.md frontmatter is missing the required description field.');
    } else if (metadata.description.length > 1024) {
        warnings.push('SKILL.md description exceeds the Agent Skills recommended maximum of 1024 characters.');
    }

    return { errors, warnings, metadata };
}

function normalizeAgentName(value) {
    if (!value) {
        return null;
    }

    const normalized = value.trim().toLowerCase();
    if (AGENTS[normalized]) {
        return normalized;
    }

    return Object.keys(AGENTS).find(agent => AGENTS[agent].aliases.includes(normalized)) || null;
}

function getSupportedAgents() {
    return Object.keys(AGENTS);
}

function getTargetGroups(agentNames, isGlobal) {
    const invalid = [];
    const groups = new Map();

    for (const rawAgent of agentNames) {
        const agent = normalizeAgentName(rawAgent);
        if (!agent) {
            invalid.push(rawAgent);
            continue;
        }

        const config = AGENTS[agent];
        const dir = isGlobal ? config.globalDir : path.resolve(config.projectDir);
        const key = `${isGlobal ? 'global' : 'project'}:${dir}`;
        const existing = groups.get(key);

        if (existing) {
            if (!existing.agents.includes(agent)) {
                existing.agents.push(agent);
                existing.labels.push(config.name);
            }
            continue;
        }

        groups.set(key, {
            dir,
            agents: [agent],
            labels: [config.name]
        });
    }

    return {
        targets: [...groups.values()],
        invalid
    };
}

module.exports = {
    AGENTS,
    DEFAULT_AGENT,
    OUTPUT_DIR,
    PROJECT_ROOT,
    SKILLS_DIR,
    SKILL_NAME_PATTERN,
    extractFrontmatter,
    getAvailableSkills,
    getSkillRecord,
    getSupportedAgents,
    getTargetGroups,
    normalizeAgentName,
    parseFrontmatter,
    validateSkillStructure
};