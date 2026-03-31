---
name: tech-doc-markdown-to-pdf
description: Convert a markdown document to a PDF file. Use when asked to "convert markdown to PDF", "export markdown as PDF", "generate a PDF from markdown", "make a PDF from .md", or when a user needs a polished PDF output from any .md file. Handles both CLI-based conversion (pandoc, wkhtmltopdf, md-to-pdf) and Node.js scripted conversion (puppeteer, markdown-pdf). Selects the best available tool automatically and applies sensible default styling.
metadata:
  domain: technical
  triggers: markdown to pdf, convert markdown, export pdf, generate pdf, md to pdf, pandoc, wkhtmltopdf, puppeteer pdf, markdown pdf, print to pdf
  role: executor
  scope: file-transformation
  output-format: file
  related-skills: content-technical-doc-coauthoring
---

# Markdown to PDF Conversion

## Overview

Convert a `.md` file to a polished PDF using the best available tool in the current environment. The output should be a clean, readable PDF suitable for sharing — not a raw browser print.

---

## Tool Selection

Check available tools in this order and use the first one found:

```
1. pandoc        — best quality; supports LaTeX, custom templates, metadata
2. md-to-pdf     — Node.js CLI; good CSS styling; no LaTeX required
3. wkhtmltopdf   — HTML-to-PDF; requires intermediate HTML step
4. puppeteer     — Node.js headless Chrome; scriptable; highest visual fidelity
```

**Check availability:**
```bash
which pandoc && echo "pandoc available"
which md-to-pdf && echo "md-to-pdf available"
which wkhtmltopdf && echo "wkhtmltopdf available"
node -e "require('puppeteer')" 2>/dev/null && echo "puppeteer available"
```

---

## Conversion Commands

### Option 1: pandoc (preferred)

```bash
pandoc input.md \
  -o output.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V mainfont="DejaVu Serif" \
  --highlight-style=tango
```

**If xelatex is unavailable, fall back to pdflatex:**
```bash
pandoc input.md -o output.pdf --pdf-engine=pdflatex -V geometry:margin=1in
```

**If no LaTeX engine is available, use wkhtmltopdf as pandoc's backend:**
```bash
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf
```

**Install pandoc if missing:**
```bash
# macOS
brew install pandoc

# Ubuntu/Debian
sudo apt-get install pandoc texlive-xetex

# Check if texlive fonts are needed
fc-list | grep -i "dejavu" || sudo apt-get install fonts-dejavu
```

---

### Option 2: md-to-pdf (Node.js)

```bash
# Install if missing
npm install -g md-to-pdf

# Convert
md-to-pdf input.md
# Output: input.pdf (same directory as input)

# Specify output path
md-to-pdf input.md --dest output.pdf
```

**Custom CSS styling via config** — add a `pdf_options` front-matter block to the markdown, or pass a config file:
```json
{
  "pdf_options": {
    "format": "Letter",
    "margin": "20mm",
    "printBackground": true
  },
  "stylesheet": "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown.min.css",
  "body_class": "markdown-body",
  "css": "body { padding: 2rem; }"
}
```

```bash
md-to-pdf input.md --config pdf-config.json
```

---

### Option 3: wkhtmltopdf

```bash
# Step 1: Convert markdown to HTML
pandoc input.md -o /tmp/input.html --standalone --metadata title="Document"
# or if pandoc unavailable:
npx marked input.md > /tmp/input.html

# Step 2: Convert HTML to PDF
wkhtmltopdf \
  --page-size Letter \
  --margin-top 20mm \
  --margin-bottom 20mm \
  --margin-left 20mm \
  --margin-right 20mm \
  --encoding utf-8 \
  /tmp/input.html output.pdf
```

**Install:**
```bash
# macOS
brew install wkhtmltopdf

# Ubuntu/Debian
sudo apt-get install wkhtmltopdf
```

---

### Option 4: puppeteer (Node.js script)

Use when maximum visual fidelity is required or when styling via CSS is preferred over LaTeX.

```javascript
// convert-md-to-pdf.js
const puppeteer = require('puppeteer');
const { marked } = require('marked');
const fs = require('fs');
const path = require('path');

async function convertToPdf(inputPath, outputPath) {
  const markdown = fs.readFileSync(inputPath, 'utf8');
  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown.min.css">
  <style>
    body { padding: 2rem 3rem; max-width: 860px; margin: 0 auto; }
    .markdown-body { box-sizing: border-box; }
    @media print { body { padding: 0; } }
  </style>
</head>
<body class="markdown-body">
${marked(markdown)}
</body>
</html>`;

  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: outputPath,
    format: 'Letter',
    margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' },
    printBackground: true,
  });
  await browser.close();
  console.log(`PDF saved to ${outputPath}`);
}

const [,, input, output] = process.argv;
const outputPath = output || input.replace(/\.md$/, '.pdf');
convertToPdf(input, outputPath).catch(console.error);
```

**Run:**
```bash
npm install puppeteer marked
node convert-md-to-pdf.js input.md output.pdf
```

---

## Naming Convention

Output PDF filename should match the input markdown filename unless the user specifies otherwise:

| Input | Output |
|-------|--------|
| `report.md` | `report.pdf` |
| `strategy-deck.md` | `strategy-deck.pdf` |
| `input/exec-memo.md` | `input/exec-memo.pdf` (same directory) |

---

## Common Issues

| Problem | Fix |
|---------|-----|
| `xelatex not found` | Use `--pdf-engine=pdflatex` or install `texlive-xetex` |
| Emojis missing in pandoc output | Use `--pdf-engine=xelatex` with `xelatex` installed |
| Tables not rendering | Add `--from=gfm` flag to pandoc to enable GitHub Flavored Markdown |
| Images broken in PDF | Use absolute paths for local images, or embed with base64 |
| Code blocks unstyled | Add `--highlight-style=tango` (pandoc) or include a CSS stylesheet |
| Chinese/Japanese/Korean characters missing | Install CJK fonts; use `--pdf-engine=xelatex` with `xeCJK` package |
| `Permission denied` writing PDF | Check that output directory exists and is writable |

---

## Quality Checklist

Before delivering the PDF, verify:

- [ ] PDF opens without errors
- [ ] All headings render at correct hierarchy
- [ ] Code blocks are formatted and readable
- [ ] Tables are not truncated
- [ ] Images appear if the source markdown included them
- [ ] Output filename matches input filename (unless overridden)
