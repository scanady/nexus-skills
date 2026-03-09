---
description: Review and ensure consistent application of Fair Code licenses across the entire project
agent: agent
---

# License Consistency Review and Enforcement

## Purpose

This prompt guides you through a comprehensive review of the OpenLife Platform to ensure that license details from LICENSE, LICENSE.md, LICENSE_EE, and LICENSE_EE.md are consistently applied throughout the project. The goal is to:

1. Remove licensing details embedded in source code files
2. Identify and fix documentation conflicts with the license model
3. Ensure consistent messaging about the Fair Code license model
4. Verify proper license file references throughout the project
5. Update any outdated or conflicting license information

**Important**: This prompt will NOT modify the actual LICENSE, LICENSE.md, LICENSE_EE, or LICENSE_EE.md files themselves.

## Context

Review the current license files to understand the project's licensing model:

#file:LICENSE
#file:LICENSE.md
#file:LICENSE_EE
#file:LICENSE_EE.md

## Requirements

### 1. **Source Code License Header Review**
   - Scan all source code files for embedded license headers or copyright notices
   - Remove detailed license text from source code files
   - Replace with simple copyright notice and reference to LICENSE file
   - Maintain file-level copyright notices where appropriate
   - Preserve any required third-party license headers

### 2. **Documentation Consistency**
   - Review README.md, CONTRIBUTING.md, and all documentation files
   - Identify language that conflicts with Fair Code license model
   - Update references to ensure consistency with LICENSE files
   - Verify Fair Code principles are accurately described
   - Check that usage scenarios match license terms

### 3. **License References**
   - Ensure all documentation properly references LICENSE and LICENSE_EE files
   - Verify links to license files are correct
   - Check that license references use consistent terminology
   - Confirm Fair Code model is properly attributed

### 4. **Enterprise Feature Identification**
   - Verify enterprise features are properly marked
   - Ensure documentation clearly identifies which features require enterprise license
   - Check that enterprise feature markers match LICENSE file descriptions
   - Validate consistency in how enterprise features are documented

### 5. **Contributor Agreement Alignment**
   - Review CONTRIBUTING file for license model consistency
   - Verify CLA terms align with dual-license model
   - Check that contributor expectations match license terms
   - Ensure no conflicting licensing language in contribution guidelines

## Expected Output

### 1. Source Code Updates

**For each source code file with embedded license headers:**

**Before (Problematic):**
```java
/*
 * Copyright (c) 2024 iFoundry Inc.
 * 
 * Licensed under the Sustainable Use License
 * 
 * You may use or modify this software only for your own internal business 
 * purposes or for non-commercial or personal use. You may distribute the 
 * software or provide it to others only if you do so free of charge for 
 * non-commercial purposes...
 * [Full license text in file]
 */
package com.openlife.platform;
```

**After (Correct):**
```java
/*
 * Copyright (c) 2024-present iFoundry Inc.
 * Licensed under the Sustainable Use License.
 * See LICENSE in the project root for license information.
 */
package com.openlife.platform;
```

**For Enterprise-licensed files:**
```java
/*
 * Copyright (c) 2024-present iFoundry Inc.
 * Licensed under the iFoundry OpenLife Enterprise License.
 * See LICENSE_EE in the project root for license information.
 */
package com.openlife.platform.enterprise;
```

### 2. Documentation Updates

Update any documentation files that have:
- Conflicting license descriptions
- Outdated license information
- Incorrect usage scenario descriptions
- Missing license references
- Ambiguous language about commercial use

### 3. Summary Report

Generate a summary of all changes made:
```markdown
# License Consistency Review Summary

## Files Modified: [count]

### Source Code Changes
- Files with license headers removed: [count]
- Files with corrected headers: [count]
- Enterprise files marked: [count]

### Documentation Updates
- README.md: [changes made]
- CONTRIBUTING.md: [changes made]
- Other docs: [list files and changes]

### Issues Identified
- [Any unresolved conflicts or questions]
- [Files that need manual review]
- [Recommendations for improvement]

### License Reference Verification
- ✓ All documentation references LICENSE files correctly
- ✓ Fair Code model described consistently
- ✓ Enterprise features properly identified
- ✓ No conflicting license language found
```

## Validation Steps

After completing the review and updates:

1. **Completeness Check**
   - [ ] All source code files reviewed for license headers
   - [ ] README.md reviewed and updated if needed
   - [ ] CONTRIBUTING.md aligned with license model
   - [ ] All documentation files checked for conflicts
   - [ ] Enterprise features clearly marked

2. **Consistency Verification**
   - [ ] License references use consistent terminology
   - [ ] Fair Code principles described accurately
   - [ ] Usage scenarios match LICENSE terms
   - [ ] No conflicting language about commercial use
   - [ ] CLA terms align with dual-license model

3. **Source Code Standards**
   - [ ] No full license text in source files
   - [ ] Copyright notices are consistent
   - [ ] License file references are correct
   - [ ] Enterprise files properly marked with LICENSE_EE
   - [ ] Third-party license notices preserved

4. **Documentation Quality**
   - [ ] License model clearly explained in README
   - [ ] Contributing guidelines reference licenses correctly
   - [ ] Fair Code links and references are accurate
   - [ ] Enterprise licensing process is clear
   - [ ] No ambiguous or misleading statements

5. **File References**
   - [ ] LICENSE file paths are correct
   - [ ] LICENSE_EE file paths are correct
   - [ ] Links to faircode.io are present and correct
   - [ ] Internal documentation links work properly

## Review Checklist

### Source Code Files to Review

Search for files with embedded license text:
```
#codebase search for: "Licensed under", "License:", "Permission is hereby granted"
```

Common locations for problematic license headers:
- Java files: `**/*.java`
- TypeScript files: `**/*.ts`, `**/*.tsx`
- JavaScript files: `**/*.js`, `**/*.jsx`
- Python files: `**/*.py`
- Configuration files with comments

### Documentation Files to Review

Priority documentation files:
- `README.md` - Primary project introduction
- `CONTRIBUTING.md` - Contributor guidelines
- `docs/**/*.md` - All documentation
- Package manifests: `package.json`, `pom.xml`, etc.
- `CODE_OF_CONDUCT.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/*.md`

### Common Conflicts to Look For

**1. Open Source Claims:**
- ❌ "This project is open source"
- ✓ "This project is fair-code / source-available"

**2. Unrestricted Use Language:**
- ❌ "Free to use for any purpose"
- ✓ "Free for internal business and non-commercial use"

**3. License Misidentification:**
- ❌ "MIT License", "Apache 2.0", "GPL"
- ✓ "Sustainable Use License" or "Fair Code"

**4. Commercial Use Ambiguity:**
- ❌ "Commercial use allowed"
- ✓ "Commercial use requires enterprise license"

**5. Contribution Rights:**
- ❌ "All contributions remain your property"
- ✓ "Contributors grant license for dual-licensing"

## Patterns and Examples

### Standard Copyright Notice for Core Features

```java
/*
 * Copyright (c) 2024-present iFoundry Inc.
 * Licensed under the Sustainable Use License.
 * See LICENSE in the project root for license information.
 */
```

### Standard Copyright Notice for Enterprise Features

```java
/*
 * Copyright (c) 2024-present iFoundry Inc.
 * Licensed under the iFoundry OpenLife Enterprise License.
 * See LICENSE_EE in the project root for license information.
 */
```

### README.md License Section Template

```markdown
## License

OpenLife Platform is [fair-code](https://faircode.io) distributed under:
- [Sustainable Use License](LICENSE) for core features
- [iFoundry OpenLife Enterprise License](LICENSE_EE) for enterprise features

This means:
- ✓ Free for internal business use
- ✓ Free for non-commercial/personal use
- ✓ Source code available for customization
- ⚠️ Commercial use requires enterprise license

For enterprise licensing inquiries: [contact email]

For more details, see our [licensing documentation](docs/licensing.md).
```

### CONTRIBUTING.md License Section Template

```markdown
## License and Contributions

By contributing to OpenLife Platform, you agree that:

1. Your contributions will be licensed under both the Sustainable Use License 
   and iFoundry OpenLife Enterprise License
2. iFoundry Inc. retains the right to offer your contributions under enterprise licensing
3. This dual-license model ensures project sustainability while rewarding contributors

All contributions are subject to our Fair Code licensing model. See [LICENSE](LICENSE) 
and [LICENSE_EE](LICENSE_EE) for details.
```

## Search and Replace Patterns

### Pattern 1: Remove Full License Text from Source Files

**Search for:**
```regex
/\*\s*Copyright.*?LICENSE[_\w]*\s*\*/
```

**Replace with:**
```
/*
 * Copyright (c) 2024-present iFoundry Inc.
 * Licensed under the Sustainable Use License.
 * See LICENSE in the project root for license information.
 */
```

### Pattern 2: Update Open Source References

**Search for variations of:**
- "open source"
- "open-source"
- "OSS"

**Review context and replace with:**
- "fair-code"
- "source-available"
- "Fair Code licensed"

### Pattern 3: Fix License URLs

**Search for:**
- Incorrect license URLs
- Broken license links
- References to wrong license types

**Replace with:**
- `[LICENSE](LICENSE)` or `[LICENSE](./LICENSE)`
- `[LICENSE_EE](LICENSE_EE)` or `[LICENSE_EE](./LICENSE_EE)`
- `https://faircode.io/`

## Execution Strategy

### Phase 1: Discovery
1. Scan all source code files for license headers
2. Scan all documentation for license references
3. Identify all conflicts and inconsistencies
4. Create inventory of files needing updates

### Phase 2: Source Code Updates
1. Update Java source files
2. Update TypeScript/JavaScript files
3. Update Python files
4. Update other language files
5. Verify no third-party license headers removed

### Phase 3: Documentation Updates
1. Update README.md
2. Update CONTRIBUTING.md
3. Update all docs/ files
4. Update GitHub templates
5. Update package manifests

### Phase 4: Verification
1. Run validation checklist
2. Search for remaining conflicts
3. Verify license references
4. Generate summary report

### Phase 5: Report and Recommendations
1. Provide summary of all changes
2. List any unresolved issues
3. Recommend additional improvements
4. Document any manual review needs

## Special Considerations

### Third-Party Code
- **DO NOT** remove license headers from third-party libraries
- Preserve all third-party copyright notices
- Verify third-party license compatibility
- Document third-party licenses if required

### Generated Code
- Code generators may insert default licenses
- Review and update generated file headers
- Consider excluding generated files from version control
- Document build process for regenerating files

### Legacy Code
- Some files may have historical copyright notices
- Preserve copyright year ranges if significant
- Update license references even in old files
- Consider adding "present" to copyright years

### Multi-Author Files
- Preserve all author copyright notices
- Consolidate under project copyright if appropriate
- Respect original author intentions
- Consider individual contributor agreements

## Tools and Automation

### Recommended Searches

**Find files with license headers:**
```
#codebase search for: "Copyright" in file type: .java,.ts,.js,.py
```

**Find "open source" references:**
```
#codebase search for: "open source" OR "open-source" in file type: .md
```

**Find license conflicts:**
```
#codebase search for: "MIT" OR "Apache" OR "GPL" in file type: .md
```

**Find commercial use language:**
```
#codebase search for: "commercial use" OR "commercial purposes"
```

### Verification Commands

**Check for remaining full license text:**
```powershell
# Search for files with suspiciously long copyright comments
Get-ChildItem -Recurse -Include *.java,*.ts,*.js,*.py | 
  Select-String -Pattern "Copyright.*\n.*\n.*\n.*\n.*\n" | 
  Select-Object -Unique Path
```

**Count files with license headers:**
```powershell
# Count files with license references
(Get-ChildItem -Recurse -Include *.java,*.ts,*.js,*.py | 
  Select-String -Pattern "Licensed under").Count
```

## Additional Notes

**Automated vs Manual Review:**
- Most source code headers can be updated programmatically
- Documentation requires careful manual review
- Context matters - don't blindly replace
- Some language is subjective and needs judgment

**Fair Code Terminology:**
- Prefer "fair-code" over "open source"
- Use "source-available" when appropriate
- Emphasize "free for internal use"
- Clarify commercial restrictions

**Community Communication:**
- Changes should maintain welcoming tone
- Explain Fair Code benefits to community
- Avoid appearing restrictive or closed
- Emphasize sustainability and fairness

**Legal Considerations:**
- These are guidance recommendations
- Review with legal counsel if uncertain
- Preserve legally required notices
- Respect third-party license requirements

## Final Report Template

```markdown
# License Consistency Review - Final Report

**Date:** [Date]
**Reviewer:** [Name/Tool]
**Project:** OpenLife Platform

## Summary
- Total files reviewed: [count]
- Files modified: [count]
- Issues resolved: [count]
- Issues requiring manual review: [count]

## Changes Made

### Source Code (files modified)
1. [File path] - [Change description]
2. [File path] - [Change description]
...

### Documentation (files modified)
1. [File path] - [Change description]
2. [File path] - [Change description]
...

## Conflicts Resolved
- [Description of conflict and resolution]
- [Description of conflict and resolution]
...

## Remaining Issues
- [Issue description and recommendation]
- [Issue description and recommendation]
...

## Verification Status
- ✓ All source files have consistent headers
- ✓ Documentation aligns with license model
- ✓ No conflicting license language found
- ✓ Enterprise features properly marked
- ✓ Fair Code model accurately described

## Recommendations
1. [Recommendation for improvement]
2. [Recommendation for improvement]
...

## Next Steps
- [ ] Review and approve changes
- [ ] Test that no functionality broken
- [ ] Update any CI/CD that checks licenses
- [ ] Communicate changes to contributors
- [ ] Consider automating future checks
```

## Success Criteria

The license consistency review is complete when:

1. **Source Code**: All source files have consistent, minimal license headers
2. **Documentation**: All docs accurately describe the Fair Code license model
3. **No Conflicts**: No conflicting license information remains
4. **Clear References**: All license references point to correct LICENSE files
5. **Enterprise Clarity**: Enterprise features are clearly identified
6. **Contributor Alignment**: CONTRIBUTING aligns with dual-license model
7. **Verification**: All validation checks pass
8. **Report Complete**: Comprehensive report generated with all changes documented

Begin the review with source code files, then move to documentation, and conclude with verification and reporting.
