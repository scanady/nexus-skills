# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. Give an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form structure
2. Create field mapping
3. Validate mapping
4. Fill the form
5. Verify output
```

## Conditional Workflows

For tasks with branching logic, guide through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```
