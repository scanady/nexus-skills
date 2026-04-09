# Designing Test Cases and Assertions

Detailed guidance on writing effective eval test cases and assertions for the skill evaluation loop.

## Test Case Design

### Prompt Quality

A test prompt should read like something a real user would type — not a formal test specification. Real users mention file paths, column names, personal context, and vary in formality.

**Strong prompts:**
- "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?"
- "there's a csv in my downloads called customers.csv, some rows have missing emails — can you clean it up and tell me how many were missing?"
- "Can you review my SKILL.md and tell me if it follows the spec? The skill is in skills/my-new-skill/"

**Weak prompts:**
- "Process this data" — too vague to test anything
- "Execute the skill's primary function with valid input" — test harness language, not user language
- "Generate output" — tells you nothing about what the user actually wants

### Coverage Strategy

Start with 2–3 test cases. Expand after the first iteration. Cover these dimensions:

| Dimension | What to Test | Example |
|-----------|-------------|---------|
| **Happy path** | Standard use case the skill is designed for | A well-formed input with clear requirements |
| **Varied phrasing** | Different levels of formality and detail | Casual ("hey can you…") vs. precise ("Parse the CSV at…") |
| **Edge cases** | Boundary conditions, malformed input | Missing data, unusual formats, ambiguous requests |
| **Trigger testing** | Whether the skill's description would activate it | Prompts using indirect language that should still trigger the skill |

### Input Files

When test cases reference files, store them in `evals/files/`:

```
evals/
├── evals.json
└── files/
    ├── sales_2025.csv
    ├── customers.csv
    └── malformed_input.json
```

Create realistic input files — not minimal stubs. The quality of test inputs directly affects the quality of eval results.

### The evals.json Schema

```json
{
  "skill_name": "csv-analyzer",
  "evals": [
    {
      "id": 1,
      "slug": "top-months-chart",
      "prompt": "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?",
      "expected_output": "A bar chart image showing the top 3 months by revenue, with labeled axes and values.",
      "files": ["evals/files/sales_2025.csv"],
      "assertions": [
        "The output includes a bar chart image file",
        "The chart shows exactly 3 months",
        "Both axes are labeled",
        "The chart title or caption mentions revenue"
      ]
    }
  ]
}
```

**Fields:**
- `id`: Sequential integer, unique within the eval set
- `slug`: Kebab-case name used for the eval directory name (e.g., `eval-top-months-chart`)
- `prompt`: The exact text given to the agent
- `expected_output`: Human-readable description of success — for context and human review, not for automated grading
- `files` (optional): Input files the prompt references
- `assertions` (optional): Added after the first run — verifiable statements about the output

## Assertion Design

### When to Write Assertions

**After** the first round of outputs, not before. You don't know what "good" looks like until the skill has run. Assertions written in a vacuum are either too vague to grade or too brittle to be useful.

### Assertion Quality Spectrum

| Quality | Example | Problem |
|---------|---------|---------|
| **Good** | "The output file is valid JSON" | Programmatically verifiable |
| **Good** | "The bar chart has labeled axes" | Specific and observable |
| **Good** | "The report includes at least 3 recommendations" | Countable |
| **Weak** | "The output is good" | Too vague to grade |
| **Weak** | "Uses exactly the phrase 'Total Revenue: $X'" | Too brittle |
| **Weak** | "The code is well-organized" | Subjective — better for human review |

### Assertion Categories

**Programmatically verifiable** — use `scripts/verify.py`:
- File existence: "The output includes a file named report.json"
- Format validity: "The output is valid JSON"
- Counts: "At least 3 sections in the response"
- String presence: "Contains the phrase 'error handling'"

**LLM-judgeable** — use the eval-grader agent:
- Semantic content: "The summary addresses the key findings from the input data"
- Structural: "The response follows the requested format with headers and bullet points"
- Completeness: "All 5 requirements from the prompt are addressed"

**Human-only** — skip assertions, present for review:
- Writing quality, tone, style
- Visual design aesthetics
- Whether the output "makes sense" holistically

### Assertion Maintenance

After each grading cycle, review assertions:

- **Always passes in both configs** → Remove. Inflates pass rate without measuring skill value.
- **Always fails in both configs** → Broken assertion, impossible task, or wrong check. Fix or remove.
- **Passes with skill, fails without** → Keep. This is the skill's value.
- **Inconsistent across runs** → Either flaky assertion or ambiguous skill instructions.

### How Many Assertions

3–6 per test case is the sweet spot. Fewer and you're not testing enough. More and you're creating maintenance burden without proportional insight.
