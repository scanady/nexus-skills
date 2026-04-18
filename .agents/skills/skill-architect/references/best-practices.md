# Skill Best Practices

---

## Output Paths Not Hard-Coded

No hard-coded output folders. Skill produces files → prompt user for root output location first.

- Skill may designate subfolders within that root (e.g., `<user-provided-root>/reports/`).
- Non-interactive skills accept output path as parameter or env var.
- Repo-root `output/` for repo-level artifacts only — skills must not reference it.

## Input Sources Not Hard-Coded

No hard-coded paths to input files or folders. Input must be:

1. Provided by user in prompt, or
2. Requested at runtime (file path, URL, or pasted content).

Skill accepts file as input → document expected format in `SKILL.md` or companion `getting-started.md`.

## Self-Contained Skills

Skill must be self-contained. All scripts, reference docs, templates, supporting files live inside skill folder.

```
skills/my-skill/
  SKILL.md
  knowledge/       # Reference docs, domain content
  scripts/         # Any runnable code
  references/      # External content that has been copied in
  getting-started.md  # (if configuration is required)
```

**Exceptions:** Skill may reference shared system tools (e.g., `node`, `python`, `git`, standard CLI utilities) expected in environment. May also reference another skill by name as suggestion (see Loose Skill Coupling). Only acceptable external dependencies.

## No Hard-Coded Credentials or API Keys

Scripts must never contain hard-coded credentials, API keys, tokens, or secrets.

- Load secrets from env vars or `.env` file at runtime.
- `.env` expected → document required vars in `getting-started.md` or `SKILL.md`.
- Never commit `.env` — add to `.gitignore`.

## Configuration Skills Require Setup Docs

Skill requires config before use (API keys, env setup, deps, tool install, etc.) → skill folder must include `readme.md` or `getting-started.md` covering:

- Prerequisites and dependencies
- Required env vars or `.env` keys
- One-time setup steps
- Minimal working example or first-run instructions

## Loose Skill Coupling

Skills may reference other skills by name to suggest companion workflow (e.g., "For deeper evaluation, consider `skill-evaluator`"). Must not depend on another skill being available.

- Every skill independently operable as standalone unit.
- Referenced skill not installed → current skill still completes task without errors or degraded output.
- Use advisory language: "You may also use…", "For deeper evaluation, consider…" — not imperative language implying hard dependency.
