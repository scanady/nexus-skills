---
description: Generate comprehensive quickstart guides (core + functional) that help users get started while showcasing project functionality, with emphasis on accuracy and progressive learning paths.
agent: agent
---

# Quickstart Guide Generator

## Purpose

Create a modular system of quickstart guides that:
1. **Enable rapid onboarding** - Users go from zero to productive in minimal time
2. **Showcase functionality** - Demonstrate core features through guided workflows
3. **Build progressively** - Each guide builds on previous knowledge
4. **Ensure accuracy** - All examples and API details verified against actual codebase
5. **Maximize user success** - Clear progression with validation at each step

## Input Variables

**Project name:** ${input:projectName:Name of the project (e.g., "Product API Service", "Authentication System")}

**Project description:** ${input:projectDescription:One-sentence description of what the project does}

**Primary tech stack:** ${input:techStack:Technologies/frameworks used (e.g., "Java 17, Spring Boot 3.2, PostgreSQL", "Node.js, Express, MongoDB")}

**Core setup steps:** ${input:coreSetupSteps:Key prerequisite steps (e.g., "Install Java/Maven, Clone repo, Start database", "Install Node/npm, Clone repo, Install dependencies")}

**Functional areas:** ${input:functionalAreas:List of main API/feature areas to document (e.g., "Product Management, Coverage Configuration, Eligibility Rules" or "User Authentication, API Key Management, Rate Limiting")}

**Number of guides:** ${input:numberOfGuides:How many functional guides? (typically 3-5, plus the core guide)}

**Target audience level:** ${input:audienceLevel:Developer experience level (e.g., "junior developers", "all levels", "experienced backend developers")}

**Estimated guide time:** ${input:estimatedTime:Target time per guide in minutes (e.g., "10-15 minutes")}

**Example API format:** ${input:apiFormat:Response format/envelope type used (e.g., JSON response wrapper, error handling pattern)}

**Prerequisite validation:** ${input:prerequisiteValidation:How to verify setup is correct (e.g., "run mvn --version, java -version", "npm --version, node -v")}

## Requirements

1. **Accuracy & Verification**
   - All API endpoints verified against actual controller code before documenting
   - Request/response payloads match DTOs and actual return types
   - HTTP methods, status codes, and error messages verified
   - Field names and data types confirmed from source code
   - All example commands tested to ensure they work

2. **Progressive Learning Path**
   - Core guide covers only setup and prerequisites (no functional workflows)
   - Each functional guide references core guide with prerequisite checklist
   - Workflows build in complexity - simple to advanced within each guide
   - Each guide includes 1-3 complete end-to-end examples
   - Cross-references between guides show relationships

3. **Functionality Showcase**
   - Demonstrate most valuable/impressive features first
   - Show real-world use cases, not just CRUD operations
   - Include advanced configurations where appropriate
   - Highlight unique capabilities that differentiate the project
   - Progressive disclosure - basic → intermediate → advanced

4. **User Success Focus**
   - Include troubleshooting sections for common errors
   - Show copy-paste ready commands (no manual modifications needed for basic flow)
   - Include expected responses so users can validate success
   - Provide clear next-steps at end of each section
   - Include validation/verification steps after key operations

5. **Documentation Quality**
   - Consistent formatting across all guides
   - Clear headers and visual hierarchy
   - Code blocks with appropriate language syntax highlighting
   - Tables for reference material (enums, error codes, parameters)
   - Links between guides using relative markdown paths

6. **Environment Coverage**
   - Address multiple deployment options if applicable (in-memory DB vs persistent, Docker vs local)
   - Include both quick-start and production-ready configurations
   - Show how to handle environment-specific differences

## Expected Output

1. **Create file: `docs/quickstart.md`**
   - Purpose: Setup and prerequisites only
   - Sections: Clone/setup, install dependencies, start environment, generate tokens/credentials
   - Length: 5-10 minutes reading time
   - Links to all functional guides
   - No workflows or features beyond basic authentication

2. **Create files: `docs/quickstart-[functional-area].md`**
   - One file per functional area (e.g., docs/quickstart-product.md, docs/quickstart-user-auth.md)
   - Each starts with "Prerequisites" section linking to core guide
   - 2-4 major workflows per guide
   - 10-15 minutes reading time each
   - Expected responses in JSON/output format
   - 1-2 troubleshooting sections per guide
   - Cross-links to related functional guides

3. **Structure Requirements**
   ```
   docs/quickstart.md                          (Core setup only)
   docs/quickstart-[functional-area-1].md      (Feature workflow 1)
   docs/quickstart-[functional-area-2].md      (Feature workflow 2)
   docs/quickstart-[functional-area-3].md      (Feature workflow 3)
   ```

4. **Content per Functional Guide**
   - Prerequisites checklist (link to core guide)
   - 2-4 numbered workflows/examples
   - Each workflow: Description → Code → Expected output → Validation
   - API endpoints reference table
   - Advanced configurations section
   - Troubleshooting section
   - Next steps pointing to other guides

## Examples

### Good Quickstart Structure

**Flow:**
1. User completes core setup (10 min)
2. User picks functional area of interest
3. User follows 3-step example (create → update → validate)
4. User sees success with actual output
5. User directed to next logical guide

**Example Progression:**
- Core: Start server ✓
- Product Guide: Create product → List products → Update product
- Coverage Guide: Add coverage to product → Configure limits → Validate amount
- Eligibility Guide: Set rules → Evaluate applicant → View results

### Example Workflow Structure

```markdown
## 1. Create a [Resource] (2 minutes)

Create a basic [resource] with required fields:

[Terminal/API command showing authentication + data]

**Expected Response**:
[JSON showing actual response structure with timestamps, IDs, etc.]

**What to note:** [Key field to save for next steps, version number, status]

---

## 2. Update the [Resource] (1 minute)

Modify the [resource] using the ID from step 1:

[Command showing version checking + update]

**Expected Response**:
[Updated JSON with new version, modified timestamp]

---

## Validation

[Command showing how to verify the change was applied]
```

### Bad vs. Good Examples

**Avoid:**
- Incomplete examples that require user to "fill in the details"
- Missing expected responses
- Commands without context about what they do
- Assuming users know about authentication token format
- Examples that work for the happy path but don't show common errors

**Instead:**
- Complete, copy-paste ready commands with real token format
- Expected responses showing exact JSON structure
- Before/after explanations
- Common error sections showing what happens when constraints are violated
- Validation step to confirm the operation succeeded

## Context References

When generating guides:

1. **Verify Against Codebase:** 
   - Search for controller methods to confirm endpoints
   - Review DTOs for request/response field names
   - Check error handling for common validation failures
   - Confirm HTTP methods and status codes

2. **Check Response Envelopes:**
   - Verify actual response structure (what fields are in metadata)
   - Confirm error response format
   - Check which fields are optional/nullable
   - Note any differences between endpoints

3. **Validate Examples:**
   - Run example commands to capture actual responses
   - Verify field values match data types
   - Check role-based access restrictions
   - Confirm prerequisite order (what must be created first)

## Validation Steps

Before finalizing guides:

1. **Accuracy Audit**
   ```
   - [ ] All endpoint paths verified against @RequestMapping/@PostMapping/@GetMapping
   - [ ] All request field names match actual DTOs
   - [ ] All response examples match actual response types
   - [ ] HTTP methods correct (GET/POST/PUT/DELETE)
   - [ ] Status codes match @ResponseStatus or ResponseEntity declarations
   - [ ] Authentication requirements correct for each endpoint
   - [ ] Error messages match actual validation rules
   ```

2. **Flow & Progression**
   ```
   - [ ] Core guide is self-contained (no external dependencies)
   - [ ] Each functional guide starts with prerequisites checklist
   - [ ] Workflows in each guide build logically (A → B → C)
   - [ ] Cross-references between guides make sense
   - [ ] No forward references to undefined concepts
   ```

3. **User Success**
   ```
   - [ ] Every code example can be copy-pasted and run
   - [ ] Every operation shows expected success response
   - [ ] Common errors documented with solutions
   - [ ] Validation steps confirm operations worked
   - [ ] Next steps guide users to logical next workflow
   ```

4. **Functionality Showcase**
   ```
   - [ ] First workflow demonstrates most impressive capability
   - [ ] Advanced sections show unique features
   - [ ] Real-world use cases included
   - [ ] Error handling not hidden - shown as part of workflow
   ```

5. **Testing**
   - Run through each guide step-by-step against live/test environment
   - Verify all code examples work without modification
   - Confirm expected responses match actual API output
   - Test troubleshooting suggestions resolve stated issues
   - Verify all cross-references point to existing guides

## Additional Notes

### Accuracy Critical Items

1. **API Response Format** - This is the #1 source of user frustration. Verify:
   - Exact field names (camelCase vs snake_case)
   - Timestamp format (ISO-8601, epoch, etc.)
   - Which metadata fields are included (timestamp, correlationId, requestId, apiVersion?)
   - Null handling (fields omitted or explicitly null?)
   - Array/object structures

2. **Required vs Optional Fields** - Check:
   - Which fields are required in requests
   - Which validation rules apply
   - What error messages are returned for invalid data
   - Default values if any

3. **Authentication/Authorization** - Verify:
   - Which endpoints require authentication
   - Which roles are required per endpoint
   - How to format the token in requests
   - What 401/403 responses look like

4. **Ordering Dependencies** - Ensure:
   - Resources are created in correct order (parent before child)
   - Examples don't reference non-existent entities
   - Prerequisite steps are actually in core guide

### Progressive Disclosure Strategy

- **Core guide:** Only setup, nothing more
- **First functional guide:** Single resource, basic CRUD (create, read, list, update)
- **Intermediate guides:** Relationships between resources, more complex operations
- **Advanced sections:** Edge cases, configuration options, optimization tips

### Common Pitfalls to Avoid

1. **Outdated examples** - Code samples must be current with codebase
2. **Assumed knowledge** - Spell out everything, don't assume familiarity
3. **Hidden prerequisites** - If something needs to exist first, say so explicitly
4. **Missing token/auth details** - Show exact format expected
5. **Incomplete workflows** - Every example should reach a verifiable success state
6. **Version mismatches** - Ensure API version numbers match actual endpoints

## Usage Instructions

After generating the guides:

1. **Verification Phase**
   - Run through core guide completely
   - Execute every command in every functional guide
   - Compare expected responses to actual API output
   - Document any discrepancies found
   - Update examples until they match exactly

2. **Validation Phase**
   - Have a new team member follow guides without help
   - Track which sections caused confusion
   - Update unclear sections
   - Ensure everyone can complete all workflows

3. **Maintenance**
   - When API changes, update examples immediately
   - Add new functional guides for new features
   - Collect user feedback and improve troubleshooting sections
   - Update cross-references if guide order changes

## Success Criteria

Guides are successful when:

✅ New users can follow core guide and be productive in target time (e.g., 10 min)
✅ Each functional guide demonstrates valuable real-world workflow
✅ Users see expected responses that exactly match API output
✅ Troubleshooting section resolves 80%+ of user issues
✅ No commands require modification to work as shown
✅ Users can link between guides to build multi-step processes
✅ Advanced sections show off unique project capabilities
✅ Zero API documentation errors in guides
