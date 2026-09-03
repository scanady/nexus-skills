# Engineering Repo Scaffolder Scripts

Repeatable, flexible automation for repository auditing, scaffolding, and reorganization against the project structure standard.

## Architecture

Four-tier structure for maintainability and flexibility:

```
assets/
├── starter/                  Starter file templates mirrored by target path
└── optional/                 Adoption-triggered templates
  └── governance/           Governance and license templates
scripts/
├── repo-audit.ps1             PowerShell audit script (Windows)
├── repo-audit.sh              Bash audit script (macOS/Linux)
├── repo-scaffold.ps1          PowerShell scaffolding script
├── repo-scaffold.sh           Bash scaffolding script
├── repo-reorganize.ps1        PowerShell reorganization script
├── repo-reorganize.sh         Bash reorganization script
└── _lib/
    ├── validators.ps1         PowerShell shared functions
    └── validators.sh          Bash shared functions
```

## Quick Start

### Prerequisites

**PowerShell (Windows):**
- PowerShell 5.1 or later (or PowerShell 7+)
- No external dependencies

**Bash (macOS/Linux):**
- Bash 4.0 or later
- `jq` (JSON parser) — install with `brew install jq` or `apt-get install jq`

### Running an Audit

**Windows (PowerShell):**
```powershell
cd scripts
.\repo-audit.ps1 -RepoRoot "C:\path\to\repo" -OutputFormat all
```

**macOS/Linux (Bash):**
```bash
cd scripts
chmod +x repo-audit.sh
./repo-audit.sh -r /path/to/repo -f all
```

**Dry run (no files written):**
```powershell
.\repo-audit.ps1 -RepoRoot "C:\path\to\repo" -DryRun
```

```bash
./repo-audit.sh -r /path/to/repo --dry-run
```

## Command Reference

### repo-audit.ps1 (PowerShell)

**Purpose:**
Read-only structural audit of a repository. Generates findings in console, JSON, and/or Markdown formats.

**Syntax:**
```powershell
.\repo-audit.ps1 [-RepoRoot <string>] [-OutputFormat <string>] [-OutputPath <string>] [-DryRun]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-RepoRoot` | Current directory | Root directory of repository to audit |
| `-OutputFormat` | `console` | Output format: `console`, `json`, `markdown`, or `all` |
| `-OutputPath` | `./audit-report` | Base path for report files (`.json` and `.md` extensions added automatically) |
| `-DryRun` | `$false` | Show what would be audited without generating reports |

**Exit Codes:**
- `0`: All checks passed
- `1`: Non-critical warnings found
- `2`: Critical issues found (starter shell incomplete)

**Example:**
```powershell
.\repo-audit.ps1 -RepoRoot "C:\projects\my-repo" -OutputFormat all -OutputPath "C:\temp\audit-results"
```

### repo-audit.sh (Bash)

**Purpose:**
Same as PowerShell version but for Unix-like systems.

**Syntax:**
```bash
./repo-audit.sh [OPTIONS]
```

**Options:**

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--repo-root` | `-r` | `.` (current directory) | Root directory of repository to audit |
| `--format` | `-f` | `console` | Output format: `console`, `json`, `markdown`, or `all` |
| `--output-path` | `-o` | `./audit-report` | Base path for report files |
| `--dry-run` | `-d` | — | Show what would be audited without generating reports |
| `--help` | `-h` | — | Show help message |

**Exit Codes:**
- `0`: All checks passed
- `1`: Any issues found

**Example:**
```bash
./repo-audit.sh -r /home/user/projects/my-repo -f all -o /tmp/audit-results
```

## Audit Phases

The audit script performs four sequential phases:

### Phase 1: Starter Shell
Verifies that all required starter-shell files exist and are non-empty:
- `README.md`
- `{project-name}.code-workspace`
- `.gitignore`
- `.agents/.gitkeep`
- `.agents/skills/.gitkeep`
- `.github/.gitkeep`
- `.github/copilot-instructions.md`
- `docs/.gitkeep`
- `docs/index.md`

The scaffold also installs configured common skills from `https://github.com/scanady/nexus-skills.git` into `.agents/skills/` unless common skill installation is skipped.

**Status:** `missing` or `empty` indicates a critical issue.

### Phase 2: Root Directory
Scans top-level files and folders to ensure they match the standard location rules.

**Detects:**
- Non-standard folders (e.g., `/config`, `/test`, `/tools`)
- Misplaced files
- Deprecated naming (e.g., `/infra` instead of `/infrastructure`)

### Phase 3: GitHub Structure
Verifies `.github/` directory exists and contains only standard assets.

### Phase 4: Documentation Structure
Verifies `docs/` directory organization follows standard conventions.

## Output Formats

### Console (Default)
Human-readable output to terminal with color coding:
- 🟢 Green: Checks passed
- 🟡 Yellow: Warnings and non-critical issues
- 🔴 Red: Critical issues

### JSON
Machine-parseable format for automation and tool integration:
```json
{
  "timestamp": "2026-05-12T14:30:00Z",
  "findingCount": 3,
  "findings": [
    {
      "path": "/config",
      "type": "non_standard",
      "status": "non_standard",
      "details": "Generic config folder violates placement principle",
      "action": "Move tool configs to root, application config near consuming code in /src, infrastructure config to /infrastructure"
    }
  ]
}
```

### Markdown
Human-readable report suitable for documentation or sharing:
```markdown
# Repository Structure Audit

**Repository:** /path/to/repo
**Generated:** 2026-05-12 14:30:00

## Summary

- Total Findings: 3
- Missing Items: 0
- Misplaced Items: 0
- Non-Standard Paths: 3

## Detailed Findings

| Path | Type | Status | Details |
|------|------|--------|---------|
| `/config` | non_standard | non_standard | Generic config folder violates placement principle |
```

## Configuration: path-rules.json

All structural rules are defined in `../references/path-rules.json` — the single source of truth for starter paths, optional template routing, and audits. Starter file contents live as individual templates in `../assets/starter/`; adoption-triggered templates live in `../assets/optional/`.

**Structure:**
```json
{
  "version": "2.3.0",
  "starter_shell": { "paths": [...] },
  "root_files": { "README.md": "...", ... },
  "root_directories": { "src": "...", ... },
  "docs_structure": { "docs/index.md": "...", ... },
  "github_structure": { ".github/copilot-instructions.md": "...", ... },
  "agents_structure": { ".agents/agents": "...", ... },
  "common_skills": { "source_url": "...", "skills": [...] },
  "non_standard_paths": { "/config": { "issue": "...", "action": "..." }, ... },
  "optional_templates": { "governance": { "CONTRIBUTING.md": "...", ... } },
  "adoption_triggers": { "CONTRIBUTING.md": "...", ... }
}
```

### Updating Rules And Templates

If the standard changes:
1. Edit `path-rules.json` when starter paths, path classifications, or audit rules change
2. Edit files under `../assets/starter/` when starter file contents change
3. Edit files under `../assets/optional/` when adoption-triggered template contents change
4. Keep path rules and template trees aligned

Audits read `path-rules.json`. Scaffold scripts read starter file contents from `../assets/starter/`. Agents should use `optional_templates` to find adoption-triggered templates.

## Shared Functions

Both platforms implement the same functions via separate language modules:

**PowerShell (validators.ps1):**
- `Get-PathRules` — Load rules from JSON
- `Test-PathExists` — Check if path exists
- `Get-RepoInventory` — List all top-level items
- `Find-NonStandardPaths` — Detect non-standard paths
- `Test-StarterShell` — Verify starter shell completeness
- `Export-Findings` — Write JSON report
- `Export-FindingsMarkdown` — Write Markdown report

**Bash (validators.sh):**
- `get_path_rules()` — Load rules from JSON
- `test_path_exists()` — Check if path exists
- `get_repo_inventory()` — List all top-level items
- `find_nonstandard_paths()` — Detect non-standard paths
- `test_starter_shell()` — Verify starter shell completeness
- `export_findings_json()` — Write JSON report
- `export_findings_markdown()` — Write Markdown report

## repo-scaffold.ps1 / repo-scaffold.sh

**Purpose:** Create the starter shell for a new repository using standard templates from `../assets/starter/`.

By default, the scaffold also installs the common skills listed in `../assets/common-skills.txt` from `https://github.com/scanady/nexus-skills.git` into `.agents/skills/`, then applies the shared engineering standards from `https://github.com/scanady/ifoundry-development.git`.

**Parameters / options:**

| PowerShell | Bash | Description |
|---|---|---|
| `-TargetPath` | `-t / --target-path` | Target directory. Default: current directory. |
| `-ProjectName` | `-n / --project-name` | Project name for stubs. Default: directory name. |
| `-DryRun` | `-d / --dry-run` | Show what would be created without writing files. |
| `-Force` | `-f / --force` | Overwrite files that already exist. |
| `-UpdateExisting` | `--update-existing` | Update existing scaffold artifacts and common skills. Equivalent to force, but clearer for alignment work. |
| `-SkipCommonSkills` | `--skip-common-skills` | Do not install common skills into `.agents/skills`. |
| `-SkillsSourceUrl` | `--skills-source-url` | Git repository for common skills. |
| `-SkillsSourceRef` | `--skills-source-ref` | Git branch, tag, or commit for common skills. |
| `-SkipSharedStandards` | `--skip-shared-standards` | Do not apply the shared standards. |
| `-StandardsSourceUrl` | `--standards-source-url` | Git repository holding the shared standards. |
| `-StandardsSourceRef` | `--standards-source-ref` | Git branch, tag, or commit for the shared standards. |

**Usage:**
```powershell
.\repo-scaffold.ps1 -TargetPath "C:\new-repo" -ProjectName "my-project"
.\repo-scaffold.ps1 -DryRun
```

```bash
./repo-scaffold.sh -t /path/to/new-repo -n "my-project"
./repo-scaffold.sh --dry-run
```

**Created files:** `README.md`, `{project-name}.code-workspace`, `.gitignore`, `.agents/.gitkeep`, `.agents/skills/.gitkeep`, `.github/.gitkeep`, `.github/copilot-instructions.md`, `docs/.gitkeep`, `docs/index.md`.

**Common skills:** `agents-nexus-skills-manager`, `skill-architect`, `skill-evaluator`, `engineering-github-repo-standards`, and `content-copy-clear-writing`. If a configured skill is missing from the source repository, the scaffold reports a warning and installs the remaining skills.

**Shared standards:** clones the standards repo and runs its `scripts/sync-standards.ps1 -TargetRepo <path>`, which adds `.github/instructions/coding-principles.instructions.md`, `core-principles.instructions.md`, and `CLAUDE.md`. The sync logic lives in that one script rather than being reimplemented here, so the bash scaffold needs `pwsh` on PATH for this step; without it the step warns and the rest of the scaffold still completes. This runs after the starter shell so the generated `CLAUDE.md` points at `.github/copilot-instructions.md`.

**Notes:** Files and skills that already exist are skipped by default. Use `-UpdateExisting` / `--update-existing` when aligning an existing project to the current scaffold standard. Use `-Force` / `--force` for the same overwrite behavior in automation. Run `repo-audit` after scaffolding to verify.

---

## repo-reorganize.ps1 / repo-reorganize.sh

**Purpose:** Generate and optionally execute a reorganization plan for an existing repository.

**Parameters / options:**

| PowerShell | Bash | Description |
|---|---|---|
| `-RepoRoot` | `-r / --repo-root` | Repository root. Default: current directory. |
| `-Execute` | `-e / --execute` | Execute the plan. Without this, only a plan is printed. |
| `-ApproveAll` | `-a / --approve-all` | Skip per-step confirmations. Requires Execute. |

**Usage:**
```powershell
# Plan only (safe — no changes)
.\repo-reorganize.ps1 -RepoRoot "C:\my-repo"

# Execute with per-step confirmation
.\repo-reorganize.ps1 -Execute

# Execute all automated steps unattended
.\repo-reorganize.ps1 -Execute -ApproveAll
```

```bash
# Plan only (safe — no changes)
./repo-reorganize.sh -r /path/to/repo

# Execute with per-step confirmation
./repo-reorganize.sh --execute

# Execute all automated steps unattended
./repo-reorganize.sh --execute --approve-all
```

**Automated step types:**
- `scaffold` — delegates to `repo-scaffold` to create missing starter-shell files
- `rename` — renames a non-standard folder (e.g., `/infra` → `/infrastructure`)

**Manual steps (printed but never auto-executed):** non-standard paths that require human judgment, such as `/config`, `/test`, `/lib`, `/tools`, `/assets`, and build output folders.

**Safety:** All moves require confirmation unless `-ApproveAll` / `--approve-all` is passed.

## Flexibility & Extension

### Running Audits Programmatically

**PowerShell:**
```powershell
. .\_lib\validators.ps1
$rules = Get-PathRules
$issues = Test-StarterShell -RepoRoot "C:\repo" -Rules $rules
```

**Bash:**
```bash
source ./_lib/validators.sh
issues=$(test_starter_shell /path/to/repo)  # uses default rules path
```

### Integrating into CI/CD

**GitHub Actions:**
```yaml
- name: Audit repository structure
  run: |
    cd .agents/skills/engineering-repo-scaffolder/scripts
    pwsh -File repo-audit.ps1 -RepoRoot "${{ github.workspace }}" -OutputFormat json
```

**Pre-commit hook:**
```bash
#!/bin/bash
cd .agents/skills/engineering-repo-scaffolder/scripts
./repo-audit.sh -r "${PWD}" -f json || exit 1
```

## Troubleshooting

### PowerShell: "Script not digitally signed"

Allow unsigned scripts for the current user:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Bash: "jq: command not found"

Install jq:
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Alpine
apk add jq
```

### Missing or empty starter shell files

The audit will flag these in Phase 1 with **critical** severity. Create the missing files using the templates in `../assets/starter/`.

## Contributing

To add new validation logic:
1. Add new rule definitions to `path-rules.json`
2. Add corresponding function(s) to both `validators.ps1` and `validators.sh`
3. Call the new function from the appropriate phase in the main script
4. Test on both Windows (PowerShell) and Unix-like systems (Bash)

To modify output formatting:
- Edit the `Format-AuditTable` / `format_audit_table` functions
- Or customize the JSON/Markdown export functions

## License

MIT — same as engineering-repo-scaffolder skill
