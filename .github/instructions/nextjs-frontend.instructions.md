---
applyTo: frontend/**
---

# Next.js Frontend Instructions

## Telemetry

**REQUIRED**: Next.js telemetry must be disabled for all projects.

When setting up a new Next.js project or after running `npm install` in an existing project, run:

```powershell
npx next telemetry disable
```

This ensures no anonymous usage data is collected from development machines.

## Configuration

- Telemetry preference is stored in `frontend/.next/cache/config.json`
- This setting persists across `npm install` runs but may need to be re-applied after clearing the `.next` cache
