# Security Patterns for Skill Evaluation

Patterns to look for when assessing security risk in agent skills.

## High-Risk Patterns in Scripts

### Network Access

```python
# Python
import requests
import urllib
import httpx
import aiohttp
urllib.request.urlopen()
requests.post()
subprocess.run(["curl", ...])
```

```javascript
// JavaScript/TypeScript
fetch("https://...")
axios.get()
http.request()
child_process.exec("curl ...")
```

```bash
# Bash
curl -X POST
wget
nc (netcat)
ssh
scp
```

### Command Execution

```python
os.system()
subprocess.run(..., shell=True)
exec()
eval()
__import__()
```

```javascript
child_process.exec()
child_process.spawn()
eval()
new Function()
```

### Credential Handling

```
# Environment variable patterns
os.environ["API_KEY"]
process.env.SECRET
$API_TOKEN
${GITHUB_TOKEN}

# File-based secrets
open(".env")
open("credentials.json")
open("~/.ssh/")
```

### File System Mutations

```python
# Dangerous write patterns
shutil.rmtree()
os.remove()
os.unlink()
open(..., "w")  # writing outside skill directory
```

### Package Installation

```bash
pip install
npm install
cargo install
apt-get install
brew install
```

## High-Risk Patterns in SKILL.md Body

### Instructions to Execute Remote Content

- "Clone this repository and run..."
- "Install the package with pip install..."
- "Fetch the latest version from..."
- "Download and execute..."

### Instructions Involving Credentials

- "Set your API key in..."
- "Configure your token..."
- "Add your credentials to..."
- "Authenticate with..."

### Instructions Modifying Shared State

- "Push to the repository..."
- "Deploy to production..."
- "Update the database..."
- "Modify the CI/CD pipeline..."
- "Send an email/message/notification..."

## Medium-Risk Patterns

### Read-Only External Access

- Fetching documentation URLs
- Reading public API endpoints (GET only)
- Cloning repos for analysis (read-only)

## Six-Dimension Safety Scoring Rubric

Apply these dimensions when generating `security_risk.sub_scores` in the catalog. Score each 1–5 (5 = safest/lowest risk).

### Data & Privacy Risk (1–5)

| Score | Signal |
|-------|--------|
| 5 | No data access. Skill is self-contained with no file reads or data handling. |
| 4 | Reads local project files only. No transmission of data externally. |
| 3 | Accesses potentially sensitive local files (config, env) but does not transmit. |
| 2 | Transmits data to external services; purpose is clear and justified. |
| 1 | Accesses, aggregates, or transmits PII or credentials without clear justification. |

### Prompt Injection / Command Hijacking Risk (1–5)

| Score | Signal |
|-------|--------|
| 5 | No dynamic input processing. Instructions are self-contained with no untrusted input injection paths. |
| 4 | Processes user input but with clear, bounded instructions. Low injection surface. |
| 3 | Instructions could be influenced by external content fetched at runtime. |
| 2 | Skill executes instructions derived from external sources or user-supplied strings without sanitization. |
| 1 | Skill is susceptible to prompt injection that could redirect agent behavior or override safety constraints. |

### Illegal or Offensive Content Risk (1–5)

| Score | Signal |
|-------|--------|
| 5 | No risk. Skill is bounded to professional/neutral domain. |
| 4 | Minor edge cases possible but not the skill's intent or workflow. |
| 3 | Skill touches content categories with moderate abuse potential (e.g., persuasive writing, opinion generation). |
| 2 | Skill could produce legally questionable or offensive outputs with minor misuse. |
| 1 | Skill explicitly assists with fraud, prohibited activities, abusive content, or illegal operations. |

### Bias or Discrimination Risk (1–5)

| Score | Signal |
|-------|--------|
| 5 | No bias exposure. Output is factual, technical, or strictly procedural. |
| 4 | Some subjective output but constrained by clear criteria. Low stereotyping risk. |
| 3 | Output involves judgment about people or groups; bias is possible but not systematic. |
| 2 | Skill encodes or amplifies stereotypes through training examples, heuristics, or categorization logic. |
| 1 | Skill systematically produces discriminatory outputs or encodes unfair treatment of groups. |

### System Integrity Risk (1–5)

| Score | Signal |
|-------|--------|
| 5 | No system mutations. Instructions are read-only or entirely in-memory. |
| 4 | Writes only to the project workspace; no system-level or shared state changes. |
| 3 | Modifies shared files, installs packages, or changes config within a controlled environment. |
| 2 | Executes system commands, modifies CI/CD pipelines, or makes deployment changes. |
| 1 | Modifies production systems, removes files destructively, or performs irreversible system-level operations without safeguards. |

### Untrusted Communication Risk (1–5)

| Score | Signal |
|-------|--------|
| 5 | No external communication. Fully offline. |
| 4 | Reads from known, trusted public sources (documentation, public APIs) via GET only. |
| 3 | Interacts with external services in a bounded, read-only way. Service identity is verifiable. |
| 2 | Sends data to external services or interacts with services whose identity is not verified. |
| 1 | Transmits sensitive data to unverified third parties, or retrieves and executes content from untrusted sources. |

### Local Script Execution

- Scripts that only read local files
- Scripts that generate output files locally
- Validation scripts that check but don't modify

### Tool Restrictions

- Skills with `allowed-tools` that limit capabilities
- Skills that explicitly prohibit network access in constraints

## Low-Risk Indicators

- No `scripts/` directory
- No URLs in SKILL.md body (or only documentation links)
- No references to environment variables or credentials
- Pure instructional content (workflow, constraints, templates)
- `allowed-tools` restricted to read-only operations
