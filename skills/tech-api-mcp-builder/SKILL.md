---
name: tech-api-mcp-builder
description: 'Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when asked to build an MCP server, create MCP tools, integrate an API with MCP, set up a protocol server, or develop an MCP integration. Supports Python (FastMCP) and Node/TypeScript (MCP SDK).'
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

# Process

## 🚀 High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Study MCP Protocol Documentation

**Navigate the MCP specification:**

Start with the sitemap to find relevant pages: `https://modelcontextprotocol.io/sitemap.xml`

Then fetch specific pages with `.md` suffix for markdown format (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages to review:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.2 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK support, broad compatibility, strong typing and linting)
- **Transport**: Streamable HTTP for remote servers (stateless JSON), stdio for local servers

**Load framework documentation:**

- **MCP Best Practices**: [Best Practices](./references/mcp_best_practices.md) - Core guidelines (tool naming, response formats, pagination, transport, security)

**For TypeScript (recommended):**
- **TypeScript SDK**: Fetch `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [TypeScript Guide](./references/node_mcp_server.md) - TypeScript patterns and examples

**For Python:**
- **Python SDK**: Fetch `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [Python Guide](./references/python_mcp_server.md) - Python patterns and examples

#### 1.3 Plan Your Implementation

**Understand the API:**
Review the service's API documentation to identify key endpoints, authentication requirements, and data models. Use web search to fetch documentation as needed.

**Tool Selection:**
Prioritize comprehensive API coverage. List endpoints to implement, starting with the most common operations.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

See language-specific guides for project setup:
- [TypeScript Guide](./references/node_mcp_server.md) - Project structure, package.json, tsconfig.json
- [Python Guide](./references/python_mcp_server.md) - Module organization, dependencies

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:**
- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints and clear descriptions
- Add examples in field descriptions

**Output/Description/Implementation/Annotations:** See the language-specific guides and [Best Practices](./references/mcp_best_practices.md) for detailed requirements on output schemas, descriptions, async patterns, error handling, pagination, and annotation hints.

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for:
- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test

**TypeScript:**
- Run `npm run build` to verify compilation
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

**Python:**
- Verify syntax: `python -m py_compile your_server.py`
- Test with MCP Inspector

See language-specific guides for detailed testing approaches and quality checklists.

---

### Phase 4: Create Evaluations

After implementing your MCP server, create comprehensive evaluations to test its effectiveness.

**Load [Evaluation Guide](./references/evaluation.md) for complete evaluation guidelines.**

#### 4.1 Understand Evaluation Purpose

Use evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

To create effective evaluations, follow the process outlined in the evaluation guide:

1. **Tool Inspection**: List available tools and understand their capabilities
2. **Content Exploration**: Use READ-ONLY operations to explore available data
3. **Question Generation**: Create 10 complex, realistic questions
4. **Answer Verification**: Solve each question yourself to verify answers

#### 4.3 Evaluation Requirements

Ensure each question is:
- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations required
- **Complex**: Requiring multiple tool calls and deep exploration
- **Realistic**: Based on real use cases humans would care about
- **Verifiable**: Single, clear answer that can be verified by string comparison
- **Stable**: Answer won't change over time

#### 4.4 Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# Reference Index

| Resource | Path | When to Load |
|----------|------|-------------|
| MCP Best Practices | [references/mcp_best_practices.md](./references/mcp_best_practices.md) | Phase 1 |
| TypeScript Guide | [references/node_mcp_server.md](./references/node_mcp_server.md) | Phase 2 |
| Python Guide | [references/python_mcp_server.md](./references/python_mcp_server.md) | Phase 2 |
| Evaluation Guide | [references/evaluation.md](./references/evaluation.md) | Phase 4 |
| TypeScript SDK README | `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` | Phase 1-2 |
| Python SDK README | `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` | Phase 1-2 |
| MCP Spec Sitemap | `https://modelcontextprotocol.io/sitemap.xml` | Phase 1 |
