# Getting Started — `<WORKFLOW_NAME>`

Manual setup steps to take a freshly imported n8n workflow from zero to running.

## 1. Prerequisites

- An n8n instance (Cloud or self-hosted, version `<MIN_VERSION>` or newer).
- Access to the services listed in **Credentials** below.
- Permission to create credentials and environment variables in your n8n instance.

## 2. Import the Workflow

1. Open n8n → **Workflows** → **Add workflow** → **Import from File**.
2. Select `<WORKFLOW_SLUG>.json`.
3. The workflow loads in **inactive** state. Do not activate yet.

## 3. Create Credentials

For each row, in n8n go to **Credentials → New** and create the named credential of the specified type, then open the workflow and assign it to each node listed.

| Credential name (suggested) | Type | Used by node(s) | Scopes / permissions |
|------------------------------|------|------------------|------------------------|
| `<CRED_1_NAME>` | `<CRED_TYPE>` | `<NODE_NAME_1>` | `<SCOPES>` |
| `<CRED_2_NAME>` | `<CRED_TYPE>` | `<NODE_NAME_2>` | `<SCOPES>` |

## 4. Set Environment Variables

Set the following on your n8n instance (Cloud: **Settings → Variables**; self-hosted: `.env` or process environment, then restart).

| Variable | Purpose | Example |
|----------|---------|---------|
| `<ENV_VAR_1>` | `<purpose>` | `<example-value>` |
| `<ENV_VAR_2>` | `<purpose>` | `<example-value>` |

## 5. External Provisioning

One-time setup in external systems:

- **<SERVICE>**: `<what to create: OAuth app, webhook endpoint, DB table, API key, etc.>`
- **<SERVICE>**: `<...>`

If the workflow uses a **Webhook** trigger, copy the Production URL from the Webhook node and register it with the upstream system.

## 6. Test the Workflow

1. Open the workflow.
2. Review any pinned sample input on the trigger node.
3. Click **Execute Workflow** (manual run).
4. Walk each node's output and verify the shape matches expectations.
5. Intentionally break a credential and confirm the **Error Trigger** subworkflow fires (if present).

Recommended test cases:

- Happy path with typical input
- Missing optional field
- External 4xx response
- External 5xx / timeout (confirm retries)

## 7. Activate

Once manual runs are clean:

1. Toggle the workflow **Active**.
2. For scheduled triggers, confirm the next run time.
3. For webhook triggers, point the upstream system at the **Production** URL (not Test).

## 8. Monitor

- Check **Executions** for the workflow — sort by failed.
- Verify the error workflow's alert channel (Slack/Email/etc.) receives a test alert.
- Tune `maxTries` / `waitBetweenTries` on external-call nodes if you see chronic retry bursts.

## 9. Known Limitations

- `<LIMITATION_1>`
- `<LIMITATION_2>`

## 10. Tuning Knobs

| Knob | Where | Default | When to change |
|------|-------|---------|-----------------|
| `maxTries` | HTTP / external-call nodes | `3–5` | Raise for flaky APIs, lower for fast-fail paths |
| `waitBetweenTries` | same | `2000` ms | Raise for rate-limited APIs |
| `executionTimeout` | workflow settings | unset | Set for long-running AI flows |
| Batch size | `Split In Batches` nodes | `50` | Lower for memory pressure, raise for throughput |

## 11. Support

- Workflow owner: `<OWNER>`
- Last updated: `<DATE>`
- Related workflows: `<LINKS>`
