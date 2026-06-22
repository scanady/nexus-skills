# Platform-Agnostic Skill Guidelines

Skills should work across any agent platform that implements the Agent Skills specification. This reference covers how to identify and resolve platform-specific coupling.

## Principles

1. **SKILL.md body stays generic** — Core workflows described in platform-neutral terms
2. **Platform details in references/** — If a skill genuinely needs platform-specific instructions, isolate them in separate reference files
3. **Use `compatibility` field** — When a skill requires specific platform features, declare it in frontmatter

## Common Platform-Specific Patterns to Avoid

### Tool References

| Platform-Specific (avoid in body) | Platform-Agnostic (preferred) |
|-----------------------------------|-------------------------------|
| "Use the Bash tool to run..." | "Run the script..." |
| "Use the Read tool to load..." | "Read the file..." |
| "Call WebFetch to..." | "Fetch the URL..." |
| "Use TodoWrite to track..." | "Track progress..." |
| "Open in VS Code terminal..." | "Run in a terminal..." |

### Platform API Assumptions

| Tied to Platform | Agnostic Alternative |
|------------------|----------------------|
| "Add to CLAUDE.md" | "Add to the project's standards file" |
| "Use GitHub Copilot inline suggestions" | "Apply the suggested changes" |
| "Run in Claude Code REPL" | "Execute the code" |

### File System Assumptions

| Tied to Platform | Agnostic Alternative |
|------------------|----------------------|
| `~/.claude/skills/` | "the skills directory" |
| `.github/copilot-instructions.md` | "the project's agent configuration" |
| Hardcoded OS-specific paths | Relative paths from skill root |

## When Platform-Specific Details Are Necessary

Some skills genuinely need platform-specific instructions. In those cases:

### Pattern: Platform Reference Files

```
my-skill/
├── SKILL.md                          # Generic workflow
└── references/
    ├── claude-code.md                # Claude Code specifics
    ├── github-copilot.md             # GitHub Copilot specifics
    └── generic-agent.md              # Fallback for other agents
```

In SKILL.md, reference conditionally:
```markdown
## Platform Setup
If your agent platform requires specific configuration, see the relevant guide:
- [Claude Code setup](references/claude-code.md)
- [GitHub Copilot setup](references/github-copilot.md)
```

### Pattern: Compatibility Field

```yaml
compatibility: Designed for Claude Code. Requires terminal access and file system permissions.
```

Use this only when the skill fundamentally depends on specific platform capabilities.

## Review Checklist for Platform Agnosticism

- [ ] SKILL.md body contains no hardcoded tool names (Bash, Read, WebFetch, etc.)
- [ ] No references to specific IDE or editor features in core workflow
- [ ] File paths are relative, not absolute or OS-specific
- [ ] Core instructions describe WHAT to do, not which platform API to call
- [ ] Platform-specific setup (if needed) is in references/ files
- [ ] `compatibility` field used when genuine platform requirements exist
- [ ] Scripts in scripts/ use standard languages (Python, Bash, JS) without platform-specific wrappers
- [ ] No assumptions about specific project config files (CLAUDE.md, .github/copilot-instructions.md) in core workflow
