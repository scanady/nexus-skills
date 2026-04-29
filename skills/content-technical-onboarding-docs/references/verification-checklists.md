# Verification Checklists

Run these checks before finalizing README, quickstart guides, and technical overview.

## Reader Journey

- The README leads with functional value, not installation or architecture.
- The README's quick start is short and ends with links into deeper guides.
- Each quickstart frames a user goal and links back to the README quick start for prerequisites.
- The technical overview is reachable from the README's additional resources and from quickstart next-steps, not from the README's main flow.
- Cross-links between README, quickstart guides, and technical overview form a clear path.

## Document Boundaries

- README contains functional content, key concepts, prerequisites, minimal quick start, contributing, license, additional resources — nothing deeper.
- Quickstart guides contain functional walkthroughs of user goals; avoid internals.
- Technical overview contains architecture, components, data flow, design decisions, code pointers — no tutorials or marketing language.

## Source Accuracy

- Project name, package name, executable names match source.
- Install commands match package manager files, build files, or scripts.
- Run commands match scripts, CLI entry points, service defs, container files, or tests.
- Env vars match config loaders, examples, compose files, or CI defs.
- Project structure descriptions match actual tree.
- Feature claims map to code, tests, route defs, or schemas.

## API Accuracy

- Endpoint paths match route or controller defs.
- HTTP methods match implementation.
- Request fields match DTOs, schemas, validators, or handler code.
- Response examples match actual return types and envelope conventions.
- Status codes match handler behavior, annotations, middleware, or tests.
- Auth requirements come from source evidence.
- Error examples use actual error response format.

## CLI Accuracy

- Commands exist in package scripts, executables, or command routers.
- Flags and options match parser defs.
- Working directory assumptions correct.
- Expected output reflects actual stdout, generated files, or side effects.
- Setup and validation commands run in documented order.

## User Success

- Every runnable example has expected output or success criterion.
- Happy-path commands copy-paste ready when possible.
- Required substitutions named explicitly and introduced before use.
- Troubleshooting tables address real failures with specific fixes.
- Time estimates, when included, realistic.

## Link and Markdown Quality

- Relative links resolve from file where they appear.
- Heading hierarchy consistent within each document.
- Tables render in GitHub-flavored Markdown.
- Code blocks declare language for syntax highlighting.
- Diagrams (when present) match surrounding prose.
- README TOC anchors match headings when manually written.

## Final Report

In completion summary, include:

- Files created or updated.
- Reader journey: README → quickstarts → technical overview.
- Commands or checks run.
- Anything not verified.
- Follow-up work to improve onboarding quality.
