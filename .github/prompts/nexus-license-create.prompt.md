---
description: Design and implement Sustainable Use License and Enterprise License files based on Fair Code licensing model
agent: agent
---

# Fair Code License Designer and Implementation

## Purpose

This prompt guides you through designing and implementing two complementary license files for your project based on the Fair Code licensing model:
1. **Sustainable Use License**: For the core/community edition with permissive internal use
2. **Enterprise License**: For enterprise/commercial features requiring separate agreements

The Fair Code model balances openness with sustainability by providing:
- Free use for internal business purposes and non-commercial use
- Full source code access for transparency and customization
- Restrictions on commercialization without agreement
- Protection for the project's long-term viability

## Project Configuration

**Project Name:** ${input:projectName:What is the name of your project? (e.g., "MyApp", "MyProject", "GreatSoftware")}

**Copyright Holder:** ${input:copyrightHolder:Who owns the copyright? (e.g., "Acme Corp", "YourCompany LLC", "Company, Inc.", "John Doe")}

**Copyright Year:** ${input:copyrightYear:What year should the copyright start? (Leave empty to use current year: 2025, or specify like "2024", "2023-present")}

**Project Description:** ${input:projectDescription:Brief description of what your software does (one sentence)}

**Enterprise Features:** ${input:enterpriseFeatures:What features/files are enterprise-only? (e.g., ".ee." in filename, "enterprise/" directory, "premium/" directory, or leave empty to use standard conventions)}

**Contact Email:** ${input:contactEmail:Email for licensing inquiries (e.g., "license@company.com")}

## Configuration Detection and Confirmation

**IMPORTANT:** Before creating any license files, you MUST:

1. **Auto-Detect Project Configuration** (where possible):
   - Search for existing `package.json`, `pom.xml`, `pyproject.toml`, `Cargo.toml`, `README.md`, or similar project files
   - Extract project name from these files if available
   - Look for copyright holders in existing files (README, package.json, etc.)
   - Check for existing LICENSE or LICENSE.md files to understand current licensing
   - Identify enterprise feature patterns (`.ee.` files, `enterprise/` directories, etc.)
   - Search for contact emails in README, CONTRIBUTING, or package files
   - If copyright year is not provided in inputs, default to the current year: **2025**

2. **Present Detected Configuration**:
   - Show all detected values to the user
   - Clearly mark which values were auto-detected vs. user-provided
   - Note any values that could not be detected and need user input
   - Present the complete configuration in a clear, structured format

3. **Request User Confirmation**:
   - Ask the user to review all detected and provided values
   - Request explicit confirmation before proceeding with license creation
   - Allow the user to correct or update any values
   - Only proceed to license generation after receiving affirmative confirmation

**Example Confirmation Message:**
```
I've detected the following project configuration:

- Project Name: [detected/provided value]
- Copyright Holder: [detected/provided value]
- Copyright Year: [detected/provided value or "2025" (current year)]
- Project Description: [detected/provided value]
- Enterprise Features: [detected patterns or "None detected"]
- Contact Email: [detected/provided value]

Please review these values and confirm:
- Are all values correct?
- Would you like to modify any of them?
- Should I proceed with creating the license files?
```

## License Structure

**Note:** Both licenses (Sustainable Use and Enterprise) will always be generated to ensure complete Fair Code licensing structure, even if no specific enterprise features are currently defined.

### 1. Sustainable Use License (LICENSE.md)

The Sustainable Use License will be created with the following structure:

**File Location:** `LICENSE` or `LICENSE.md` in project root

**Core Components:**
1. **License Header**: Project name, copyright, and license overview
2. **Acceptance**: Agreement to terms by using the software
3. **Copyright License**: Grants to use, modify, distribute, and create derivatives
4. **Limitations**: Restrictions on commercial use
5. **Patents**: Patent grant and termination conditions
6. **Notices**: Requirements for preserving license notices
7. **No Other Rights**: Clarification that no additional rights are granted
8. **Termination**: Conditions for license termination and reinstatement
9. **No Liability**: Disclaimer of warranties and liability
10. **Definitions**: Clear definitions of key terms

**Key Principles:**
- Free for internal business use
- Free for non-commercial/personal use
- Free distribution for non-commercial purposes
- Cannot be commercialized or sold without agreement
- Must preserve license notices
- Source code available for modification

### 2. Enterprise License (LICENSE_EE.md)

The Enterprise License will be created for commercial/enterprise features:

**File Location:** `LICENSE_EE` or `LICENSE_EE.md` in project root

**Core Components:**
1. **License Header**: Enterprise license identifier
2. **Copyright Notice**: Copyright holder and year
3. **Usage Restrictions**: Production use requires valid enterprise license
4. **Development Exception**: Free use for development and testing
5. **Modification Rights**: Rights to create modifications and patches
6. **Ownership**: All modifications owned by licensor
7. **Redistribution**: Restrictions on redistribution
8. **Warranty Disclaimer**: Standard disclaimer
9. **Third-Party Components**: Notice about third-party licenses

**Key Principles:**
- Production use requires paid license
- Free for development and testing
- All modifications owned by copyright holder
- Cannot redistribute without license
- Protects commercial viability

## Requirements

### 1. **Legal Accuracy**
   - Use clear, plain English while maintaining legal validity
   - Follow established Fair Code license templates
   - Ensure terms are enforceable and unambiguous
   - Include all necessary legal protections

### 2. **Project-Specific Customization**
   - Insert project name throughout licenses
   - Include correct copyright holder and year
   - Reference appropriate enterprise feature identifiers (if applicable)
   - Add correct contact information for inquiries

### 3. **File Organization**
   - Create separate files for each license type
   - Use standard naming conventions (LICENSE.md, LICENSE_EE.md)
   - Include clear headers and section markers
   - Format with proper Markdown structure

### 4. **Enterprise Feature Identification**
   - Clearly define what code is covered by each license
   - Specify file naming patterns or directory structures for enterprise code
   - Document how to identify enterprise-only features
   - Provide examples if applicable

### 5. **Documentation Integration**
   - Include guidance on how licenses apply
   - Reference Fair Code model and principles
   - Provide links to additional information
   - Explain usage scenarios (allowed vs. restricted)

## Expected Output

Create the following files in the project root:

### 1. LICENSE or LICENSE.md
Complete Sustainable Use License with:
- Project-specific header identifying the software
- Copyright notice with holder and year
- Full license text based on Sustainable Use License template
- Clear definitions section
- Contact information for licensing questions

### 2. LICENSE_EE or LICENSE_EE.md
Complete Enterprise License with:
- Enterprise license identifier
- Copyright notice
- Production use restrictions
- Development/testing exception
- Modification and ownership terms
- Contact information for enterprise licenses

**Note:** This file is always generated to support future enterprise features and maintain complete Fair Code licensing structure.

### 3. (Optional) LICENSE_NOTICE.md
Summary document explaining:
- Which parts of the codebase use which license
- How to identify enterprise vs. core features
- Common usage scenarios and what's allowed
- How to obtain an enterprise license
- Link to Fair Code principles

### 4. Review and Update CONTRIBUTING or CONTRIBUTING.md

**Critical Requirement**: Ensure the CONTRIBUTING file aligns with the Fair Code license model.

**Review Existing File:**
1. Check if `CONTRIBUTING` or `CONTRIBUTING.md` exists in the project root
2. Read the existing content to understand current contribution guidelines
3. Identify any conflicts with Fair Code licensing model

**Key Elements to Add/Update:**

**Contributor License Agreement (CLA) Section:**
```markdown
## Contributor License Agreement

By contributing to this project, you agree to the following terms:

1. **License Grant**: You grant [COPYRIGHT HOLDER] a perpetual, worldwide, non-exclusive, 
   royalty-free, irrevocable license to use, copy, modify, distribute, and sublicense 
   your contributions under the project's license terms.

2. **Dual License Rights**: You acknowledge that [COPYRIGHT HOLDER] has the right to 
   license the software under both the Sustainable Use License and the [PROJECT NAME] 
   Enterprise License, and your contributions may be included in both versions.

3. **Ownership**: You retain ownership of your contributions, but grant [COPYRIGHT HOLDER] 
   the rights necessary to distribute and monetize the project.

4. **Representations**: You represent that you have the legal right to grant the above 
   license and that your contribution does not violate any third-party rights.

5. **No Obligation**: [COPYRIGHT HOLDER] is under no obligation to accept your contributions.
```

**License Clarification Section:**
```markdown
## Understanding the License Model

This project uses a Fair Code license model:

- **Sustainable Use License**: Core features are freely available for internal business 
  and non-commercial use
- **Enterprise License**: Commercial use and enterprise features require a separate license
- **Your Contributions**: Will be available under both licenses, ensuring the project's 
  long-term sustainability

### What This Means for Contributors

- You can freely use the software for internal and non-commercial purposes
- Your contributions help the entire community
- The copyright holder can offer enterprise licenses using your contributions
- This model ensures the project remains financially viable and well-maintained
```

**Attribution Section:**
```markdown
## Attribution

All contributors will be acknowledged in:
- The project's contributor list
- Release notes for versions including their contributions
- The project website/documentation (if applicable)

We value and recognize all community contributions while maintaining the licensing 
structure that ensures project sustainability.
```

**Contribution Process Alignment:**
Ensure the contribution process mentions:
- Code contributions are subject to review
- Acceptance criteria include license compliance
- All PRs must include CLA acknowledgment
- Enterprise feature contributions require discussion first

**Remove or Update Conflicting Language:**
- Remove any references to "Apache 2.0" or "MIT" licenses if present
- Update any language suggesting contributors retain all rights
- Clarify that contributions don't automatically grant commercial usage rights to others
- Remove language that conflicts with dual-license model

**Example Updated CONTRIBUTING.md Structure:**
```markdown
# Contributing to [PROJECT NAME]

## Welcome

We appreciate your interest in contributing! This guide explains how to contribute 
while respecting our Fair Code license model.

## License and Contributor Agreement

### Understanding Our License Model
[Include explanation of Fair Code, Sustainable Use License, and Enterprise License]

### Contributor License Agreement
[Include CLA terms as shown above]

### By Contributing You Agree
When you submit a pull request or contribution, you agree to the Contributor License 
Agreement above. No separate signature is required - your PR submission constitutes 
acceptance.

## How to Contribute

### Types of Contributions
[Existing contribution guidelines]

### Code Contributions
[Existing code contribution process]

### Documentation
[Existing documentation guidelines]

## Attribution
[Include attribution policy as shown above]

## Questions?

For licensing questions: [contact email]
For contribution questions: [contribution contact]
```

**Validation Checklist for CONTRIBUTING:**
- [ ] CLA terms are clearly stated
- [ ] Dual-license model is explained
- [ ] Contributors understand their contributions can be used in enterprise version
- [ ] Attribution policy is clear
- [ ] No conflicting license terms remain
- [ ] Process for accepting contributions respects Fair Code model
- [ ] Enterprise feature contribution process is documented
- [ ] Questions/contact information provided

## Fair Code Principles Reference

Your licenses should embody these Fair Code principles:

**Free and Sustainable:**
- Free use for internal business purposes
- Free use for non-commercial/personal purposes
- Sustainable through commercial restrictions

**Open but Pragmatic:**
- Full source code access
- Can be modified and extended
- Pragmatic restrictions protect viability

**Community meets Prosperity:**
- Community benefits from open source
- Creators can monetize commercial use
- Business relationships benefit both parties

**Meritocratic and Fair:**
- Contributors respected and valued
- Fair compensation for commercial use
- Sustainable model for maintainers

## License Templates

### Sustainable Use License Template

```markdown
# License

## Sustainable Use License

Portions of this software are licensed as follows:

• [Content structure based on your enterprise feature organization]
• All other content is available under the "Sustainable Use License" as defined below.

## Sustainable Use License

Version 1.0

### Acceptance

By using the software, you agree to all of the terms and conditions below.

### Copyright License

The licensor grants you a non-exclusive, royalty-free, worldwide, non-sublicensable, non-transferable license to use, copy, distribute, make available, and prepare derivative works of the software, in each case subject to the limitations below.

### Limitations

You may use or modify the software only for your own internal business purposes or for non-commercial or personal use. You may distribute the software or provide it to others only if you do so free of charge for non-commercial purposes. You may not alter, remove, or obscure any licensing, copyright, or other notices of the licensor in the software. Any use of the licensor's trademarks is subject to applicable law.

### Patents

The licensor grants you a license, under any patent claims the licensor can license, or becomes able to license, to make, have made, use, sell, offer for sale, import and have imported the software, in each case subject to the limitations and conditions in this license. This license does not cover any patent claims that you cause to be infringed by modifications or additions to the software. If you or your company make any written claim that the software infringes or contributes to infringement of any patent, your patent license for the software granted under these terms ends immediately. If your company makes such a claim, your patent license ends immediately for work on behalf of your company.

### Notices

You must ensure that anyone who gets a copy of any part of the software from you also gets a copy of these terms. If you modify the software, you must include in any modified copies of the software a prominent notice stating that you have modified the software.

### No Other Rights

These terms do not imply any licenses other than those expressly granted in these terms.

### Termination

If you use the software in violation of these terms, such use is not licensed, and your license will automatically terminate. If the licensor provides you with a notice of your violation, and you cease all violation of this license no later than 30 days after you receive that notice, your license will be reinstated retroactively. However, if you violate these terms after such reinstatement, any additional violation of these terms will cause your license to terminate automatically and permanently.

### No Liability

As far as the law allows, the software comes as is, without any warranty or condition, and the licensor will not be liable to you for any damages arising out of these terms or the use or nature of the software, under any kind of legal claim.

### Definitions

The "licensor" is the entity offering these terms.

The "software" is the software the licensor makes available under these terms, including any portion of it.

"You" refers to the individual or entity agreeing to these terms.

"Your company" is any legal entity, sole proprietorship, or other kind of organization that you work for, plus all organizations that have control over, are under the control of, or are under common control with that organization. Control means ownership of substantially all the assets of an entity, or the power to direct its management and policies by vote, contract, or otherwise. Control can be direct or indirect.

"Your license" is the license granted to you for the software under these terms.

"Use" means anything you do with the software requiring your license.

"Trademark" means trademarks, service marks, and similar rights.
```

### Enterprise License Template

```markdown
# The [PROJECT NAME] Enterprise License (the "Enterprise License")

Copyright (c) [YEAR] [COPYRIGHT HOLDER].

With regard to the [PROJECT NAME] Software:

This software and associated documentation files (the "Software") may only be used in production, if you (and any entity that you represent) hold a valid [PROJECT NAME] Enterprise license corresponding to your usage. Subject to the foregoing sentence, you are free to modify this Software and publish patches to the Software. You agree that [COPYRIGHT HOLDER] and/or its licensors (as applicable) retain all right, title and interest in and to all such modifications and/or patches, and all such modifications and/or patches may only be used, copied, modified, displayed, distributed, or otherwise exploited with a valid [PROJECT NAME] Enterprise license for the corresponding usage. Notwithstanding the foregoing, you may copy and modify the Software for development and testing purposes, without requiring a subscription. You agree that [COPYRIGHT HOLDER] and/or its licensors (as applicable) retain all right, title and interest in and to all such modifications. You are not granted any other rights beyond what is expressly stated herein. Subject to the foregoing, it is forbidden to copy, merge, publish, distribute, sublicense, and/or sell the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For all third party components incorporated into the [PROJECT NAME] Software, those components are licensed under the original license provided by the owner of the applicable component.
```

## Usage Scenarios

### Allowed Under Sustainable Use License:
1. **Internal Business Use**: Using the software within your company for internal operations
2. **Personal/Non-Commercial Use**: Using for personal projects, learning, experimentation
3. **Modifications**: Creating custom modifications for internal use
4. **Contributions**: Contributing improvements back to the project
5. **Consulting Services**: Offering consulting, implementation, or support services
6. **Integration**: Creating integrations with other tools and systems
7. **Free Distribution**: Sharing the software free of charge for non-commercial purposes

### Restricted (Requires Enterprise License):
1. **Hosted Services**: Offering the software as a paid hosted/SaaS service
2. **White Labeling**: Rebranding and selling as your own product
3. **Reselling**: Charging customers to access or use the software
4. **Managed Services**: Providing managed instances as a paid service
5. **Commercial Embedding**: Embedding in commercial products where the software provides core value

### Development and Testing:
- Always free for development, testing, and evaluation purposes
- No license required for non-production environments
- Enterprise features can be tested before purchasing

## Context

This prompt creates Fair Code licenses following these established models:
- Sustainable Use License (as used by projects in the Fair Code community)
- Enterprise License patterns from commercially sustainable open source projects
- Fair Code principles: https://faircode.io/

The model balances:
- **Openness**: Full source code access, free internal use, community collaboration
- **Sustainability**: Commercial restrictions ensure project viability
- **Fairness**: Contributors compensated for commercial use, users have freedom for internal use

## Validation Steps

After generating the licenses:

1. **Completeness Check**
   - [ ] Both LICENSE and LICENSE_EE files exist in project root
   - [ ] All project-specific variables replaced (name, copyright, year, email)
   - [ ] Enterprise feature identification clearly documented
   - [ ] All sections present in each license
   - [ ] CONTRIBUTING file reviewed and updated for Fair Code compliance
   - [ ] CLA terms added to CONTRIBUTING file

2. **Accuracy Verification**
   - [ ] Copyright holder and year are correct
   - [ ] Project name appears consistently throughout
   - [ ] Contact information is accurate
   - [ ] Enterprise feature markers match your codebase structure

3. **Language Review**
   - [ ] Text is clear and readable
   - [ ] Legal terminology is used correctly
   - [ ] Definitions section covers all key terms
   - [ ] No ambiguous or contradictory statements

4. **Integration Check**
   - [ ] Licenses reference each other appropriately (if applicable)
   - [ ] README references the license model
   - [ ] CONTRIBUTING file exists and aligns with Fair Code model
   - [ ] CONTRIBUTING file includes CLA terms
   - [ ] CONTRIBUTING file explains dual-license model to contributors
   - [ ] No conflicting license terms in CONTRIBUTING file
   - [ ] Enterprise features properly marked in codebase

5. **Documentation**
   - [ ] Usage scenarios documented
   - [ ] How to obtain enterprise license explained
   - [ ] Fair Code principles referenced
   - [ ] Links to additional information included

## Contributor License Agreement (CLA) Considerations

**Why CLA is Important for Fair Code:**
- Ensures copyright holder can offer both community and enterprise licenses
- Protects contributors from liability
- Clarifies ownership and usage rights
- Enables license flexibility (e.g., changing licenses if needed)
- Standard practice for projects with dual-license models

**CLA Implementation Options:**
1. **Implicit CLA**: Terms in CONTRIBUTING.md, acceptance via PR submission (recommended for most projects)
2. **Explicit CLA**: Separate document requiring signature (for larger organizations)
3. **CLA Bot**: Automated GitHub bot that requires acknowledgment before PR merge

**Best Practices:**
- Keep CLA terms simple and clear
- Explain WHY the CLA is needed (sustainability, dual-license model)
- Don't make it more complex than necessary for your project size
- Provide contact information for questions
- Consider adding CLA terms to PR template

## Additional Notes

**Important Legal Considerations:**
- These templates are provided as-is and should be reviewed by legal counsel
- Adapt terminology to match your jurisdiction if needed
- Consider adding jurisdiction-specific clauses if required
- Keep licenses up-to-date as Fair Code model evolves
- CLA terms should be reviewed by legal counsel for enforceability

**Fair Code Community:**
- Consider listing your project at https://faircode.io/
- Join discussions with other Fair Code projects
- Share learnings and improvements with the community
- Contribute to evolving the Fair Code model

**Enterprise License Pricing:**
- Decide on your enterprise pricing model before launch
- Consider volume pricing, user-based, or feature-based tiers
- Document pricing clearly for potential enterprise customers
- Provide easy path to contact sales/licensing team

**Enforcement:**
- Monitor for commercial use without proper licensing
- Establish process for handling violations
- Consider offering grace periods for unintentional violations
- Build relationships with commercial users

## Examples

### Example 1: Basic Project with No Enterprise Features

For a project without separate enterprise features yet:

**LICENSE**:
```markdown
# License

Copyright (c) 2024-present Acme Corp.

This software is licensed under the Sustainable Use License.

[Full Sustainable Use License text...]
```

**LICENSE_EE**: (Still generated to support future enterprise features and maintain Fair Code structure)

### Example 2: Project with Enterprise Directory

For a project with enterprise features in specific directories:

**LICENSE**:
```markdown
# License

Portions of this software are licensed as follows:

• Content within the `/enterprise` directory is NOT licensed under the Sustainable Use License. 
  To use code within `/enterprise`, you must hold a valid MyApp Enterprise License.
• All other content is available under the "Sustainable Use License" as defined below.

[Full license text...]
```

### Example 3: Project with File Naming Convention

For a project using `.ee.` in filenames for enterprise features:

**LICENSE**:
```markdown
# License

Portions of this software are licensed as follows:

• Source code files that contain ".ee." in their filename or ".ee" in their directory name 
  are NOT licensed under the Sustainable Use License. To use such files, you must hold 
  a valid MyApp Enterprise License as defined in LICENSE_EE.
• All other content is available under the "Sustainable Use License" as defined below.

[Full license text...]
```

## Support and Resources

**Fair Code Resources:**
- Fair Code website: https://faircode.io/
- Fair Code principles and FAQ
- Examples from existing Fair Code projects

**License Questions:**
- For licensing questions: [Contact email from input]
- For enterprise licensing: [Enterprise contact from input]

**Community:**
- Consider providing community forum for license questions
- Document common scenarios in FAQ
- Share success stories and use cases
