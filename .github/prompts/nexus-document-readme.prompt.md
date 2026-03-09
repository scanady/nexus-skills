---
agent: agent
description: 'Create or update a comprehensive README.md for the project that focuses on overview and links to quickstart guides for getting started'
---

## Role

You are an expert product manager. Your goal is to generate or update a highly informative, engaging, and well-structured README.md file that serves as the project overview and entry point to documentation.

## Task

1.  **Check for existing README.md**: First, look for an existing README.md file in the project root.
2.  **Analyze the project**: Review the entire project workspace and codebase to understand architecture, features, and capabilities.
3.  **Check for quickstart guides**: Look for `quickstart.md` and `quickstart-*.md` files in the project root.
4.  **Generate or Update**:
  * If README.md exists: Preserve existing content where appropriate, update outdated sections, and add missing sections.
  * If README.md doesn't exist: Create a new comprehensive README.md from scratch.
5.  Include all the following essential sections, ensuring correct heading and link formatting:
  * **Title and Description** (Project Name and Goal)
  * **Badges** (Build/status, version, and license badges)
  * **Quick Links** (If quickstart guides exist, link to them prominently)
  * **Table of Contents** (Linked to all main sections)
  * **Features & Capabilities** (What makes this project unique/valuable)
  * **Architecture Overview** (High-level system design, key components)
  * **Key Concepts** (Important ideas/patterns used in the project)
  * **Project Structure** (Folder/file organization)
  * **Prerequisites & Requirements** (What needs to be installed, system requirements)
  * **Getting Started** (Link to quickstart guides OR brief setup if no guides exist)
  * **Contributing** (Guide on forking, branching, and pull requests)
  * **License** (Reference the License)
  * **Additional Resources** (Links to docs, API reference, etc.)

## Guidelines

### Project Details

* **Project Name:** [INSERT YOUR PROJECT NAME HERE]
* **Project Goal/Summary:** [BRIEFLY DESCRIBE WHAT YOUR PROJECT DOES - focus on the WHY and WHAT, not HOW]
* **Technologies Used:** [E.g., Node.js/npm, Python/Pip, Docker, Java/Maven, React, etc.]
* **Quickstart guides exist:** [YES/NO - If yes, links will be prominent]

### Formatting and Structure

- Use clear headers (`#`, `##`, `###`) to ensure GitHub's auto-generated table of contents works.
- Format all commands and code examples using triple backticks (\`\`\`).
- Ensure all links in the Table of Contents are properly formatted with hyphens for anchor links.
- Use GitHub Flavored Markdown
- Use relative links (e.g., `docs/CONTRIBUTING.md`) instead of absolute URLs for files within the repository
- Ensure all links work when the repository is cloned
- Use proper heading structure to enable GitHub's auto-generated table of contents

### Quickstart Guides Strategy

**IF quickstart guides exist** (`quickstart.md` and `quickstart-*.md` files):
- Place prominent "Quick Links" section early in README pointing to:
  * Core guide: `quickstart.md` for setup and prerequisites
  * Functional guides: `quickstart-[feature].md` for working with specific features
- **Do NOT duplicate** content from quickstart guides in README
- **Do NOT include** Installation or Usage instructions with code examples
- Instead, README should provide:
  * High-level project overview
  * Architecture and design concepts
  * Feature highlights (conceptual, not procedural)
  * Links to quickstart guides for hands-on tutorials

**IF NO quickstart guides exist**:
- Include traditional Installation and Usage sections with code examples
- Provide basic getting-started instructions in README itself
- Note that these should eventually be moved to dedicated quickstart guides

### Update Strategy (if README.md exists)

* Preserve user-written content in sections like badges, acknowledgments, or custom sections.
* Update technical details (installation, usage) to reflect current codebase.
* Ensure consistency in formatting throughout.

### What NOT to include

* Do not include the full license text, only the reference.
* Do NOT duplicate installation/usage instructions if quickstart guides exist - link to them instead
* Do NOT include step-by-step code examples if they're covered in quickstart guides
* Do NOT repeat "how to get started" if covered in quickstart.md
* Do NOT create long tutorials or workflows - these belong in quickstart guides
* Keep README focused on WHAT the project does and WHY, not HOW to use it

### What TO emphasize in README

* **Project overview** - What problem does it solve?
* **Key features** - What can you do with this project?
* **Architecture** - How is it organized? What are the main components?
* **Design patterns** - What patterns/concepts are used?
* **Quick links** - Where should users go next? (Link to quickstart guides)
* **Contributing** - How to contribute to the project
* **Prerequisites** - What needs to be installed before getting started

Analyze the codebase and project structure to make the generated content accurate and helpful for both new users and contributors. Focus on providing high-level understanding that complements the hands-on quickstart guides.