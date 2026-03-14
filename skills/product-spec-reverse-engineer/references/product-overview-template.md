# Product Overview Template

Use this template to structure the product overview document. This is the executive-level document — concise, non-technical, focused on what the system does and why it matters.

## Document Structure

### 1. Executive Summary
2-3 sentences maximum. Answer:
- What is this system?
- Who does it serve?
- What is the core value proposition?

Do NOT name the product. Use "the system" or "the platform."

### 2. Problem Statement
One paragraph covering:
- What problem exists without this system
- Who experiences this problem
- What the consequences of the problem are

Derive this from the features and workflows discovered in the codebase — infer the problem from the solution.

### 3. Solution Overview
One paragraph describing at a high level how the system addresses the problem. Cover:
- The approach (not the technology)
- What makes this approach effective
- The scope of what the system handles

### 4. Key Capabilities
A bulleted list of 5-10 major capabilities, each as a single sentence:
- **[Capability Name]:** [One sentence describing what users can do]

Order by importance to the end user. Group related capabilities with a blank line between groups if natural groupings exist.

### 5. User Roles
A brief table — simpler than the functional spec version:

| Role | Description |
|------|-------------|
| [Generic role name] | [One sentence — what this user does in the system] |

### 6. System Context
A brief description of where this system sits in a broader ecosystem:
- What external systems does it connect to (by function, not vendor)
- What data flows in and out
- Is it standalone or part of a larger platform

Keep to 3-5 bullet points.

### 7. Key Workflows
Describe 2-4 primary workflows at a very high level (3-5 steps each, no technical detail):

#### [Workflow Name]
1. [User does X]
2. [System responds with Y]
3. [Outcome Z]

Choose workflows that best illustrate the system's core value.

### 8. Quality & Operational Characteristics (Optional)
Only include if clearly observable from the codebase. One bullet each:
- Scalability approach
- Security posture
- Reliability patterns
- Compliance considerations

## Tone & Style
- Write for a non-technical executive or product stakeholder
- No jargon, no framework names, no architecture terms
- Every sentence should be understandable by someone with no engineering background
- Focus on outcomes and user value, not mechanisms
- Keep the entire document under 2 pages when rendered
