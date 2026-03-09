---
description: Performs a comprehensive project review covering system design, code quality, and documentation for release readiness.
agent: agent
---

# Comprehensive Project Review & Release Readiness Report

## Context
You are an expert software design engineer. Your goal is to perform a comprehensive review of the project to prepare the solution for release. This includes analyzing system design, code structure, documentation consistency, and overall completeness.

## Input Variables
- Focus Area: ${input:focusArea:Specific area to focus on (e.g., 'security', 'performance', 'all') - default: 'all'}
- Report Path: ${input:reportPath:Path to save the review report - default: 'docs/release-review-report.md'}

## Requirements

1. **System Design Analysis**
   - Analyze the project structure (Maven/Spring Boot) and adherence to standard practices.
   - Review `pom.xml` for dependencies, versions, and potential conflicts.
   - Check `docker-compose.yml` and `Dockerfile` for containerization best practices and environment consistency.
   - Review database configuration, connection pooling, and migration scripts (`src/main/resources/db/migration`).

2. **Code Design & Quality**
   - Evaluate adherence to the "Package-by-feature" structure mentioned in `.github/copilot-instructions.md`.
   - Check for consistent coding standards and patterns in `src/main/java`.
   - Review test coverage, test types (Unit, Contract), and test configuration in `src/test/java`.
   - Identify potential code smells, anti-patterns, or technical debt.

3. **Documentation Consistency & Completeness**
   - Verify `README.md` instructions against the actual project structure and available commands.
   - Check the `docs/` folder for outdated, conflicting, or missing information.
   - Validate that API specifications in `specs/` align with the actual implementation.
   - Ensure `.github/copilot-instructions.md` is accurate and up-to-date.

4. **Release Readiness**
   - Check Spring profiles (`dev`, `demo`, `prod`) in `src/main/resources` for correct configuration separation.
   - Verify security configurations (JWT, secrets management, CORS).
   - Ensure the build process (`mvn package`) is reliable and documented.
   - Check for any hardcoded credentials or environment-specific paths.

## Expected Output

1. **Generate Report:** Create a comprehensive Markdown report at `${input:reportPath}` containing:
   - **Executive Summary:** A high-level assessment of the project's state.
   - **Detailed Findings:** A section for each requirement category (System Design, Code Quality, Documentation, Release Readiness) detailing observations and issues.
   - **Recommendations:** Actionable steps to fix identified issues, prioritized by impact.
   - **Release Status:** A clear "Go/No-Go" recommendation with justification.

## Context References
- Project Instructions: #file:../.github/copilot-instructions.md
- Documentation: #file:../README.md
- Build Configuration: #file:../pom.xml
- Codebase: #codebase

## Validation Steps
After generating the report:
1. Verify that the file exists at `${input:reportPath}`.
2. Ensure the report contains all required sections: Executive Summary, Detailed Findings, Recommendations, and Release Status.
3. Check that specific file paths and code references in the report are linked correctly.
