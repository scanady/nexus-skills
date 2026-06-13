# Principles — Distilled

The principles cited in `SKILL.md`, expanded with the spirit of where they come from. Use this when defending a recommendation, when teaching the team, or when picking between two principles in tension.

These are not rules to follow blindly — they are lenses. Apply the lens that surfaces the most useful question for the situation in front of you.

---

## Andrej Karpathy — Strip it to the math

Spirit: prefer systems you understand deeply enough to make simple. If a design only works while hidden behind ceremony, keep reducing it until the moving parts are obvious.

**The smallest model that works.** Karpathy's instinct, sharpened on neural networks and compilers, is to find the simplest configuration that solves the problem and resist anything more. A two-layer MLP that works tells you something a hundred-layer transformer that also works does not. In code review: prefer the minimum viable shape — fewer modules, fewer types, fewer configurations — and only add structure when current structure fails on a real problem.

**First principles, not cargo cult.** When asked why something is built a certain way, "best practice" or "the framework wants it" is not an answer. Reduce to: what does this code need to do, what is the cheapest correct shape for doing it, and why does the current shape deviate from that? If the deviation is unjustified, that is the finding.

**Distillation.** A good abstraction is the *smallest* one that captures the pattern, not the most general. Most abstractions are premature — they encode a guess about future variation that never arrives. Compress what is repeated; do not pre-generalize what is not.

**Understand before optimizing.** Most performance "optimizations" optimize the wrong thing. Read the code, sketch the data flow, identify the actual hot path. If you cannot say *why* a change makes things faster, the change is speculative.

**Software 2.0 mindset.** Some problems are better solved by data and search than by hand-written rules. In code review, the analog is: ask whether a problem is being solved with overgrown procedural code that should be a table lookup, a config, a state machine, or a generated artifact.

---

## Boris Cherny — Make it ergonomic, edit it surgically

Spirit: good tools and good changes reduce friction. They compose with the maintainer's intent instead of demanding a new way to work.

**Surgical change.** Cherny's instinct — sharpened on developer tools where each edit must compose with the user's intent — is that targeted edits beat sweeping refactors. A 10-line change that removes a bug or a layer is worth more than a 1000-line "cleanup". Mass renames, formatter flips, and structural reorganizations create churn without changing behavior, and they make every future merge harder.

**Iterative pragmatism.** Get the simplest version working end-to-end, then iterate based on actual feedback. Premature design — picking the architecture before the system has shown you its shape — usually constrains the wrong axes.

**Short feedback loops.** A multi-minute test run, a flaky local setup, a build that requires three terminals — these compound across every other improvement the team will ever make. Fixing the feedback loop is often the highest-leverage change in a codebase, and it is almost always under-prioritized because it is invisible to outsiders.

**Ergonomic tools.** APIs, CLIs, error messages, default values, and config files are read more often than they are written. Optimize for the reader. A flag named `--quiet` is better than `--no-verbose`; an error that explains what to do is better than a stack trace; a default that is right 90% of the time is worth more than configurability that is exercised 1% of the time.

**Types and contracts as documentation.** Where the language allows, encode intent in the type. A typed boundary is easier to refactor than an untyped one because the compiler tells you what broke. Avoid `any`-equivalent escape hatches in public APIs.

---

## Thomas Dohmke — Remove friction, let people ship

Spirit: teams move faster when obstacles disappear. Treat setup, unclear errors, and hidden workflow knowledge as real engineering problems.

**Developer experience is a feature, not a polish item.** Setup friction, unclear errors, missing scripts, undocumented prerequisites — these are not "nice to haves later." They are the gate between a contributor and their first pull request. Fix them with the same seriousness as a bug.

**Ship > perfect.** A working v1 in production beats a perfect v2 in a branch. Reserve polish for proven leverage. The signal "this is working and people are using it" beats almost any internal quality argument.

**Remove the obstacle, do not add another tool.** When a workflow is painful, the first instinct should be to delete the source of the pain (a manual step, an unnecessary config, a redundant build) — not to add a new tool that automates the pain.

**Empower, do not gatekeep.** A codebase that requires tribal knowledge to navigate fails new contributors. Conventions, naming, and structure should be guessable. If onboarding requires a person, the system has a documentation or design defect.

**Open and inspectable.** Even in private codebases, the same instinct applies: prefer plain files, plain text, plain protocols over opaque configurations and proprietary glue. Readable systems are maintainable systems.

---

## Common Thread

All three converge on a small set of operating defaults:

1. **Subtraction is design.** The best change is often deletion. Code, layers, configs, dependencies, tests, ceremony — all candidates.
2. **The smallest viable change.** Patch, not rewrite. Add structure only when current structure fails a real workload.
3. **Optimize the path the human takes.** Setup, build, test, debug, deploy. Friction here taxes every future change.
4. **Ground every recommendation in the actual system.** Not in trend, not in taxonomy, not in what the recommender would have built from scratch.

---

## Tensions and How to Resolve Them

These principles can pull against each other. When they do:

| Tension | Default |
|---|---|
| "Smallest change" vs "fix the feedback loop" | If feedback loop friction is hurting *every* change, fix it first — it pays compound interest |
| "Surgical change" vs "the whole module is wrong" | Recommend the surgical change for the bug now; flag the module as a separate, lower-priority finding |
| "Conventions over preferences" vs "the conventions are bad" | Only break a convention if you can name the concrete cost of keeping it; otherwise match it |
| "Ship > perfect" vs "this isn't done" | Ship if it solves the user's problem and the gaps are documented and bounded; do not ship if it silently fails |
| "Distillation" vs "more abstractions" | Wait for the third repetition before abstracting; two is a coincidence, three is a pattern |
