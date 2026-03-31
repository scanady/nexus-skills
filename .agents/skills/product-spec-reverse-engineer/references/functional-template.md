# Functional Specification Template

Use this template to structure the functional specification document. Every section is required unless explicitly marked optional.

## Document Structure

### 1. System Overview
Write 2-3 paragraphs covering:
- What the system does (core purpose)
- Who it serves (target users/audience categories)
- What value it provides (the problem it solves)
- How it fits into a broader ecosystem (if applicable)

Do NOT name the product. Use "the system" or "the platform" as the subject.

### 2. User Roles & Permissions
Present as a table:

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| [Generic role name] | [What this user type does] | [Comma-separated list of capabilities] |

Include:
- All distinct roles discovered in auth/permission code
- Anonymous/unauthenticated access if applicable
- System/service accounts if they initiate actions

### 3. Functional Areas
Group by **user-facing capability**, not by code module. Each functional area follows this structure:

#### [Capability Name]
- **Purpose:** One sentence — what value this provides to users
- **Actors:** Which roles interact with this capability
- **Trigger:** What initiates the workflow (user action, schedule, event, API call)
- **Preconditions:** What must be true before this can execute
- **Flow:**
  1. [Step — describe what the user does and what the system does in response]
  2. [Step]
  3. [Step]
- **Business Rules:**
  - [Rule — validation logic, constraints, conditional behavior]
- **Edge Cases:**
  - [Case — what happens when inputs are invalid, limits are reached, dependencies fail]
- **Outputs:** What the user sees, receives, or what state changes occur

**Naming convention for capabilities:**
- Use verb-noun pairs: "Manage Users", "Process Payments", "Generate Reports"
- Group related sub-capabilities under a parent heading
- Order by user journey (onboarding → core usage → administration)

### 4. Data Entities
Describe in plain language — no SQL, no schema syntax.

For each core entity:
- **Name:** Generic functional name (e.g., "User Account" not "users table")
- **Purpose:** Why this entity exists
- **Key Attributes:** Important fields described functionally (e.g., "unique identifier", "display name", "creation timestamp")
- **Relationships:** How it connects to other entities (e.g., "A user account owns zero or more projects")
- **Lifecycle:** How it is created, modified, and retired

### 5. Integration Points
For each external system the product connects to:
- **Function:** What role this integration serves (e.g., "email delivery", "payment processing")
- **Direction:** Inbound, outbound, or bidirectional
- **Trigger:** What causes the integration to fire
- **Data Exchanged:** What information flows between systems
- **Failure Behavior:** What happens when the integration is unavailable

### 6. Business Rules Summary
Cross-cutting rules that span multiple functional areas:
- Naming format: BR-001, BR-002, etc.
- Each rule: condition → action → exception (if any)
- Group by domain (user management, data processing, security, etc.)

### 7. Non-Functional Observations (Optional)
Only include if observable from the codebase:
- Performance characteristics (caching, pagination, rate limiting)
- Data retention or archival patterns
- Audit logging
- Accessibility considerations
