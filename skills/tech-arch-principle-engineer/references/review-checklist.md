# Review Checklist — What to Read, What to Look For

A structured pass for reviewing a sizeable codebase. Use it when you need coverage; skip sections that are not relevant. The checklist is a tool, not a rubric — every item should produce a finding only if it surfaces real leverage.

---

## Pass 1 — Frame (5–10 minutes)

Goal: be able to write the "System read" section of the report in 2–3 sentences.

- [ ] `README.md` (or equivalent) — what does the project claim to do?
- [ ] Top-level docs / `docs/` / `design/` — is there a stated north star, charter, or design overview?
- [ ] `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` — what runtime, what dependencies, what scripts?
- [ ] `LICENSE` and contributors — open source, internal, solo, team?
- [ ] Recent commits (last 20–50) — what is currently being worked on? where is the activity?

If you cannot summarize the system after this pass, **ask** before continuing. Reviewing what you do not understand produces noise.

---

## Pass 2 — Survey (15–30 minutes)

Goal: understand the system's *shape* and locate the seams.

### Entry points
- [ ] `main`, `cli`, `index`, `app`, `server` — where does execution begin?
- [ ] What is the public API surface? (exports, routes, commands)
- [ ] How many entry points are there, and do they share state?

### Module structure
- [ ] How many top-level modules / packages?
- [ ] What is the directory depth? (deep nesting often hides organizational confusion)
- [ ] Where does domain logic live vs glue / plumbing?
- [ ] Ratio of glue to domain — is most of the code wiring things together?

### Data flow
- [ ] What is the primary data type that flows through the system?
- [ ] Where does data enter, where does it exit?
- [ ] How many transformations between entry and exit?
- [ ] Are transformations co-located or scattered?

### Tests
- [ ] Where do tests live? How many?
- [ ] Test:code line ratio (rough)
- [ ] What kind of tests dominate — unit, integration, e2e?
- [ ] Read 2–3 test files end-to-end — they reveal *intended* behavior more honestly than code or docs

### Build & dev loop
- [ ] How does a developer set up the project? Is there a one-command setup?
- [ ] How long does the test suite take?
- [ ] How long does a build take?
- [ ] Are there pre-commit hooks, linters, formatters? Do they run fast?

### Dependencies
- [ ] Count direct dependencies. Anything obviously redundant? (two HTTP libraries, two test runners, etc.)
- [ ] Are there heavy dependencies (frameworks, ORMs) doing work that could be plain code?
- [ ] Any abandoned or unmaintained dependencies?

---

## Pass 3 — Diagnose

The diagnostic prompts below are ordered by typical leverage. Stop early if you are finding signal — a long checklist is a temptation to over-report.

### A. Missing simplicity (highest leverage, usually)

- [ ] Is there code that could disappear without changing behavior?
- [ ] Configurations that no one tunes?
- [ ] Tests that test the framework instead of the code?
- [ ] Docs that duplicate what the code already says?
- [ ] Layers that exist "for separation" but only have one implementer?

### B. Premature abstraction

- [ ] Interfaces / abstract classes / traits with exactly one implementer
- [ ] Factory functions that build one type
- [ ] Generic types parameterized by `<T>` where `T` is always the same thing
- [ ] Plugin systems with one plugin
- [ ] Configurable behavior that has never been configured

### C. Indirection without payoff

- [ ] Wrapper around wrapper around standard library
- [ ] Async / callback / event for what is fundamentally synchronous
- [ ] Message bus / event emitter for two static endpoints
- [ ] Dependency injection container for three dependencies
- [ ] Inheritance hierarchies more than two levels deep

### D. Slow feedback loops

- [ ] Test suite > 30 seconds for unit tests, > 2 minutes for full
- [ ] Build > 10 seconds for incremental
- [ ] Hot reload broken or absent
- [ ] Local dev requires multi-step manual setup
- [ ] Errors are unclear (stack traces with no context, opaque framework errors)

### E. Friction in the developer path

- [ ] Setup steps not in `README` or scripted
- [ ] Required env vars undocumented
- [ ] No `getting-started.md` or first-run guide
- [ ] Errors that do not say what to do next
- [ ] Default values that are wrong for 80%+ of cases

### F. Concentrated complexity

- [ ] Files > 500 lines of non-trivial code
- [ ] Functions > 50 lines doing distinct things
- [ ] Classes / modules with > 10 public methods
- [ ] Cyclomatic hotspots — branching logic that could be a state machine, table, or polymorphism

### G. Untestable seams

- [ ] Code that hard-codes I/O (file paths, network calls, time, randomness) without injection
- [ ] Singletons or module-level state that tests must reset
- [ ] Tests that require a real database / network / browser to verify pure logic

### H. Dead and stale

- [ ] Unused exports, unused dependencies, unused config keys
- [ ] Commented-out code blocks (use VCS, not comments)
- [ ] TODOs older than a year
- [ ] Docs that contradict the code
- [ ] Tests for removed features

### I. Internal inconsistency

- [ ] Two patterns for the same problem (e.g., two ways of handling errors)
- [ ] Naming that drifts (`getUser`, `fetchAccount`, `loadProfile` for the same operation)
- [ ] File layout inconsistent across modules
- [ ] Mix of paradigms (functional in one place, OO-with-inheritance in another) without reason

---

## Pass 4 — Quick Greps

Useful when you need to scan a large codebase fast. Run them, scan the output, follow up only on real signal.

| Pattern | Why look |
|---|---|
| `TODO`, `FIXME`, `XXX`, `HACK` | Concentration of these = neglected debt zones |
| `any`, `unknown`, `interface{}`, `Object`, `void *` | Type escape hatches in public APIs |
| `try { } catch {}` (empty catch) | Silenced errors |
| `process.env` / `os.environ` accessed deep in code | Hidden config dependencies |
| `setTimeout` / `sleep` in tests | Flaky tests, racy code |
| `eval`, dynamic `require`, dynamic `import(name)` | Plugin systems, often premature |
| Class hierarchies > 2 levels | Inheritance abuse |
| Files imported from > 5 different layers | Over-coupling |

---

## Pass 5 — Synthesis

- [ ] List every candidate finding
- [ ] Score each on **impact × ease**
- [ ] Cut everything below the top three unless it is genuinely an error (not a preference)
- [ ] For each surviving finding: name the principle, write the surgical fix, predict the outcome
- [ ] Write the "What NOT to do" section — it is as important as the recommendations
- [ ] Re-read the report with one question: *would the maintainer of this system feel respected and helped?* If not, rewrite.
