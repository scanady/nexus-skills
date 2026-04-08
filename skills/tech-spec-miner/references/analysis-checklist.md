# Analysis Checklist

## Comprehensive Checklist

| Area | What to Find | Glob/Grep Patterns |
|------|--------------|-------------------|
| **Entry points** | Main executables, app boots, startup files | `**/main.*`, `Program.cs`, `manage.py`, `Cargo.toml` |
| **Routes** | Controllers, route files, URL declarations | `**/routes/**/*`, `**/controllers/**/*`, `**/urls.py`, `@Controller` |
| **Models** | Entities, schemas, migrations, ORM config | `**/models/**/*`, `**/entities/**/*`, `schema.prisma`, `@Entity` |
| **Auth** | Guards, middleware, JWT, OAuth, policy checks | `**/auth/**/*`, `**/middleware/**/*`, `passport`, `jwt`, `Authorize` |
| **Validation** | DTOs, validators, serializers, request schemas | `**/dto/**/*`, `**/serializers/**/*`, `@IsString`, `pydantic`, `validate` |
| **Error handling** | Exception filters, rescue/catch blocks, error mappers | `ExceptionFilter`, `catch`, `rescue_from`, `@ControllerAdvice` |
| **External calls** | HTTP clients, SDK usage, queues, RPC | `fetch(`, `axios.`, `requests.`, `grpc`, `WebClient` |
| **Config** | Env files, config modules, app settings, build files | `**/.env*`, `**/config/**/*`, `application.yml`, `appsettings.json` |
| **Tests** | Test files reveal behaviors and edge cases | `**/tests/**/*`, `**/test/**/*`, `**/*.{spec,test}.*` |
| **Background jobs** | Queues, schedulers, workers, cron tasks | `@Cron`, `Bull`, `Queue`, `Celery`, `Sidekiq`, `Hangfire` |

## Analysis Phases

### Phase 1: Structure Discovery
- [ ] Identify technology stack
- [ ] Map directory structure
- [ ] Find entry points
- [ ] List all modules/packages

### Phase 2: API Surface
- [ ] Document all endpoints
- [ ] Note HTTP methods and paths
- [ ] Identify request/response formats
- [ ] Find authentication requirements

### Phase 3: Data Layer
- [ ] Map all data models
- [ ] Document relationships
- [ ] Find migrations
- [ ] Note validation rules

### Phase 4: Business Logic
- [ ] Trace main flows
- [ ] Identify business rules
- [ ] Document state transitions
- [ ] Find external integrations
- [ ] Capture evidence links for each significant behavior

### Phase 5: Security
- [ ] Check authentication method
- [ ] Review authorization patterns
- [ ] Find input validation
- [ ] Note security configurations

### Phase 6: Quality & Testing
- [ ] Review existing tests
- [ ] Note test coverage
- [ ] Document error handling
- [ ] Find logging patterns
- [ ] Note whether evidence comes from runtime-facing code, tests, or both

## Verification Questions

Before finalizing specification:

- [ ] All endpoints documented?
- [ ] All models mapped?
- [ ] Authentication flow clear?
- [ ] Error responses documented?
- [ ] External dependencies listed?
- [ ] Uncertainties flagged?
- [ ] Code locations attached to significant observations?
