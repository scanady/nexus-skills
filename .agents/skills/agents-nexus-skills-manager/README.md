# Nexus Skills Manager

Operational skill for installing, upgrading, exporting, listing, syncing, and troubleshooting Nexus Skills from either a cloned `nexus-skills` repository or an external consumer project.

## What it manages

- Project-scoped skill installs
- Global skill installs
- Agent targets: `agent-skills`, `github-copilot`, `claude-code`, and `codex`
- Skill-specific, pack-specific, and broad installs
- Upgrade confirmation and installed-copy replacement
- Export packaging for manual import
- Common install and routing troubleshooting

## Package structure

```text
agents-nexus-skills-manager/
├── SKILL.md
├── README.md
├── references/
│   ├── cli-reference.md
│   ├── install-workflows.md
│   └── troubleshooting.md
├── evals/
│   ├── evals.json
│   └── trigger-queries.json
└── scripts/
    └── validate_package.py
```

## Validation

Run from this skill directory:

```bash
python scripts/validate_package.py .
```

The validator checks required files, frontmatter, bundled references, and evaluation JSON shape.