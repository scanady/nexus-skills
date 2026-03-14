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
