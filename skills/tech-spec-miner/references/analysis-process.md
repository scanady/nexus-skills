# Analysis Process

Use these patterns as a starting point, not a hardcoded script. Pick the patterns that match the repository's language, framework, and shape.

## Step 1: Project Structure

```bash
# Find entry points
Glob: **/main.{ts,js,tsx,jsx,py,go,java,cs,rb,rs}
Glob: **/app.{ts,js,py,rb}
Glob: **/index.{ts,js,tsx,jsx}
Glob: **/Program.cs
Glob: **/*Application.{java,kt}
Glob: **/manage.py
Glob: **/Cargo.toml

# Find routing and request entry patterns
Glob: **/routes/**/*.{ts,js,py,rb,go}
Glob: **/controllers/**/*.{ts,js,java,kt,cs,rb}
Glob: **/views.py
Glob: **/urls.py
Grep: @Controller|@Get|@Post|router\.|app\.(get|post|put|delete)|Route::|urlpatterns|Map(Get|Post|Put|Delete)|http\.HandleFunc
```

## Step 2: Data Models

```bash
# Database schemas
Glob: **/models/**/*.{ts,js,py,java,kt,cs,rb,go}
Glob: **/entities/**/*.{ts,js,java,kt,cs}
Glob: **/schema*.{ts,js,py,sql,rb}
Glob: **/migrations/**/*
Glob: **/prisma/schema.prisma
Grep: @Entity|class.*Model|schema\s*=|CREATE TABLE|DbSet<|belongs_to|has_many|struct .*Model
```

## Step 3: Business Logic

```bash
# Services and logic
Glob: **/services/**/*.{ts,js,py,java,kt,cs,rb,go}
Glob: **/use-cases/**/*
Glob: **/handlers/**/*
Glob: **/processors/**/*
Grep: async.*function|export.*class|class .*Service|def .*\(|func .*\(|impl .*\{|module .* do
```

## Step 4: Authentication & Security

```bash
# Auth patterns
Glob: **/auth/**/*
Glob: **/guards/**/*
Glob: **/middleware/**/*
Grep: @Guard|middleware|passport|jwt|Authorize|Authentication|SpringSecurity|Devise|before_action|CSRF|oauth
```

## Step 5: External Integrations

```bash
# External calls
Grep: fetch\(|axios\.|HttpService|request\(|httpx\.|requests\.|Faraday|RestTemplate|WebClient|HttpClient|grpc
Glob: **/integrations/**/*
Glob: **/clients/**/*
Glob: **/adapters/**/*
```

## Step 6: Configuration

```bash
# Config files
Glob: **/*.config.{ts,js,py,rb}
Glob: **/.env*
Glob: **/config/**/*
Glob: **/application*.{yml,yaml,properties}
Glob: **/appsettings*.json
Glob: **/pyproject.toml
Glob: **/package.json
Glob: **/pom.xml
Glob: **/build.gradle*
Glob: **/Cargo.toml
```

## Step 7: Tests And Operational Clues

```bash
# Test files reveal supported behaviors and edge cases
Glob: **/*.{spec,test}.{ts,js,tsx,jsx,py,rb,go}
Glob: **/test/**/*
Glob: **/tests/**/*
Grep: describe\(|it\(|pytest|RSpec|@Test|TestCase

# Logging, jobs, and background work reveal runtime behavior
Grep: logger\.|log\.|@Cron|Queue|Bull|Sidekiq|Celery|Hangfire|schedule|worker
Glob: **/jobs/**/*
Glob: **/workers/**/*
Glob: **/tasks/**/*
```

## Quick Reference

| Pattern | Purpose |
|---------|---------|
| `**/main.*`, `Program.cs`, `manage.py` | Entry points |
| `**/routes/**/*`, `**/controllers/**/*`, `**/urls.py` | API and routing surfaces |
| `**/models/**/*`, `**/entities/**/*`, `schema.prisma` | Data models |
| `**/tests/**/*`, `**/*.{spec,test}.*` | Executable behavior clues |
| `**/jobs/**/*`, `**/workers/**/*` | Background processing |
