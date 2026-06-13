# Common `applyTo` Glob Patterns

Reference for constructing `applyTo` frontmatter in path-specific instructions files.

## Syntax Rules

- Patterns are matched against file paths relative to the repository root
- Multiple patterns are separated by commas (no spaces after comma)
- Standard glob syntax: `*` (single segment), `**` (recursive), `?` (single char)

## By Language

| Language | Pattern | Notes |
|----------|---------|-------|
| TypeScript | `**/*.ts,**/*.tsx` | Include both `.ts` and `.tsx` |
| JavaScript | `**/*.js,**/*.jsx` | Include both `.js` and `.jsx` |
| Python | `**/*.py` | |
| Java | `**/*.java` | |
| C# | `**/*.cs` | |
| Go | `**/*.go` | |
| Rust | `**/*.rs` | |
| Ruby | `**/*.rb` | |
| PHP | `**/*.php` | |
| Swift | `**/*.swift` | |
| Kotlin | `**/*.kt,**/*.kts` | Include script files |
| SQL | `**/*.sql` | |
| CSS/SCSS | `**/*.css,**/*.scss` | |
| HTML | `**/*.html,**/*.htm` | |
| Markdown | `**/*.md` | |
| YAML | `**/*.yml,**/*.yaml` | |
| Shell | `**/*.sh,**/*.bash` | |

## By Framework / Directory

| Target | Pattern | Notes |
|--------|---------|-------|
| React components | `src/components/**/*.tsx` | Scoped to component directory |
| Next.js app | `app/**/*.tsx,app/**/*.ts` | App Router files |
| Next.js pages | `pages/**/*.tsx,pages/**/*.ts` | Pages Router files |
| Django models | `**/models.py,**/models/**/*.py` | Both single-file and package models |
| Django views | `**/views.py,**/views/**/*.py` | |
| Spring Boot | `src/main/java/**/*.java` | Main source only |
| Rails models | `app/models/**/*.rb` | |
| Rails controllers | `app/controllers/**/*.rb` | |
| Express routes | `src/routes/**/*.ts` | |
| Flutter | `lib/**/*.dart` | |

## By Concern

| Concern | Pattern | Notes |
|---------|---------|-------|
| Tests (general) | `**/*.test.*,**/*.spec.*,**/test_*` | Common test patterns |
| Tests (Python) | `**/test_*.py,**/*_test.py,tests/**/*.py` | pytest conventions |
| Tests (Java) | `src/test/**/*.java` | Maven/Gradle convention |
| Tests (JS/TS) | `**/*.test.ts,**/*.test.tsx,**/*.spec.ts` | |
| Migrations (SQL) | `**/migrations/**/*.sql` | |
| Migrations (ORM) | `**/migrations/**/*.py,**/migrations/**/*.ts` | |
| Config files | `**/*.config.*,**/.*rc,**/.*rc.*` | |
| API routes | `**/api/**,**/routes/**` | |
| Documentation | `docs/**/*.md,**/*.md` | |
| Docker | `**/Dockerfile,**/docker-compose*.yml` | |
| CI/CD | `.github/workflows/**/*.yml` | GitHub Actions |
| Infrastructure | `**/terraform/**/*.tf,**/infra/**` | IaC files |

## Pattern Composition Examples

Combine patterns for precise targeting:

```yaml
# All frontend TypeScript
applyTo: "frontend/**/*.ts,frontend/**/*.tsx"

# All backend Java excluding tests
applyTo: "backend/src/main/**/*.java"

# All test files across languages
applyTo: "**/*.test.*,**/*.spec.*,**/test_*.*"

# Specific subdirectory
applyTo: "src/api/**/*.ts"

# Multiple related directories
applyTo: "src/models/**/*.ts,src/schemas/**/*.ts,src/types/**/*.ts"
```

## Wildcard Reference

| Pattern | Matches | Example |
|---------|---------|---------|
| `*` | Any file in current directory | `*.py` → `foo.py` but not `dir/foo.py` |
| `**` | Any file recursively | `**/*.py` → `foo.py` and `dir/foo.py` |
| `**/*` | Same as `**` | |
| `?` | Single character | `test_?.py` → `test_a.py` |
| `{a,b}` | Alternation | `*.{ts,tsx}` → `.ts` or `.tsx` |
| `src/**` | Everything under src | All files and subdirectories |
