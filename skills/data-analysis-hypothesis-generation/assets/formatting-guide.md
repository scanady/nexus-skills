# Hypothesis Report — Formatting Guide

Quick reference for the LaTeX template (`hypothesis-report-template.tex`) and style package (`hypothesis_generation.sty`). Compile with **XeLaTeX or LuaLaTeX** (not pdfLaTeX — the boxes and fonts need it).

## Quick Start

```latex
% !TEX program = xelatex
\documentclass[11pt,letterpaper]{article}
\usepackage{hypothesis_generation}
\title{Your Phenomenon Name}
\begin{document}
\maketitle
% content
\end{document}
```

Compile: `xelatex file` → `bibtex file` → `xelatex file` → `xelatex file`.

## Colors

Hypotheses (one color, used consistently for that hypothesis throughout): H1 deep blue · H2 forest green · H3 royal purple · H4 teal · H5 burnt orange. Utility: predictions amber · evidence light blue · comparisons steel gray · limitations coral red.

## Box Environments

| Environment | Use for |
|-------------|---------|
| `summarybox` | executive summary (top of document) |
| `hypothesisbox1`…`5` | each competing hypothesis (mechanism + evidence + assumptions) |
| `predictionbox` | testable predictions per hypothesis |
| `comparisonbox` | how to distinguish two hypotheses |
| `evidencebox` | highlight key supporting evidence (use sparingly; detail → Appendix A) |
| `limitationbox` | important limitations/challenges |

Each takes an optional title: `\begin{hypothesisbox1}[Hypothesis 1: Title] … \end{hypothesisbox1}`.

**Hypothesis box pattern** (keep to ≤0.6 pages):
```latex
\newpage
\begin{hypothesisbox1}[Hypothesis 1: Title]
\textbf{Mechanistic Explanation:} [1--2 brief paragraphs, 6--10 sentences]
\textbf{Key Supporting Evidence:}
\begin{itemize}\item [point] \citep{ref1}\item [point] \citep{ref2}\end{itemize}
\textbf{Core Assumptions:}
\begin{enumerate}\item [assumption]\end{enumerate}
\end{hypothesisbox1}
```

**Prediction box:** state the prediction, then bullets for Conditions / Expected Outcome / Falsification. **Comparison box:** Fundamental Difference → Discriminating Experiment → Outcome Interpretation (if A → HX, if B → HY).

## Document Structure

**Main text — 4 pages maximum, highly selective:**
1. Executive summary (`summarybox`, 0.5–1 pg)
2. Competing hypotheses (`hypothesisbox*`, one per hypothesis, 3–5 total, 2–2.5 pg) — brief mechanism + 2–3 evidence bullets + 1–2 assumptions
3. Testable predictions (`predictionbox`, 1–2 per hypothesis, 0.5–1 pg)
4. Critical comparisons (`comparisonbox`, highest-priority only, 0.5–1 pg)

**Appendices (comprehensive):** A literature review (40–60+ citations) · B experimental designs (full protocols) · C quality assessment (tables + strengths/weaknesses) · D supplementary evidence. Target **50+ total references**, the vast majority in appendices; main text carries 10–20 key citations (`\citep{}` / `\citet{}`).

## Preventing Page Overflow

`tcolorbox` environments **do not break across pages** — content exceeding the remaining space overflows. Rules:
- Put `\newpage` before each hypothesis box (and before any long box).
- Keep each main-text box ≤0.6 pages; move detail to appendices.
- Use `\newpage` between major appendix sections and `\clearpage` before the appendix block.
- Visually check the compiled PDF for overflow.

## Tables

```latex
\begin{hypotable}{Caption}
\begin{tabular}{|l|l|}
\hline \tableheadercolor \textcolor{white}{\textbf{Header}} & \textcolor{white}{\textbf{Header}}\\\hline
row & data\\\hline \tablerowcolor row & data\\\hline
\end{tabular}\caption{Caption}
\end{hypotable}
```
`\tableheadercolor` for header rows, `\tablerowcolor` to alternate shading. Use `p{width}` columns and `\small` for wide tables.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `.sty not found` | keep `hypothesis_generation.sty` beside the `.tex` (or on the LaTeX path) |
| boxes have no color | compile with XeLaTeX/LuaLaTeX, not pdfLaTeX |
| citations show `[?]` | run `bibtex` after the first `xelatex`, then `xelatex` twice more |
| fonts not found | leave the `\setmainfont`/`\setsansfont` lines commented out |
| content overflows | `\newpage` before the box; shorten it; move detail to appendices |
| main text > 4 pages | move mechanism detail and extra evidence to Appendix A |

Required packages: `tcolorbox` (most), `xcolor`, `fontspec`, `fancyhdr`, `titlesec`, `enumitem`, `booktabs`, `natbib`.

## Style Consistency

Same color per hypothesis throughout · reserve boxes for key content · consistent numbering (H1, prediction P1.1, comparison H1 vs H2) · precise, specific, quantitative language · group multiple citations `\citep{a,b,c}`.
