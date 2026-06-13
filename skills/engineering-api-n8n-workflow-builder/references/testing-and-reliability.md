# Testing and Reliability Patterns

Load when designing test strategy and reliability features (Step 2 and Step 5 validation).

## Test Strategy

### 1. Pinned Data

Pin representative input on the trigger node so you can re-run the workflow manually without re-triggering the source system.

In the JSON:

```json
"pinData": {
  "Webhook": [
    { "json": { "userId": "u_123", "amount": 42.50 } }
  ]
}
```

Include at least one pinned sample per trigger for any non-trivial workflow.

### 2. Test Cases to Cover

For every workflow, plan these manual test runs:

- **Happy path** — typical valid input
- **Empty / missing field** — required field absent
- **Oversized input** — large array, long string
- **External 4xx** — 400 / 401 / 404 from an API
- **External 5xx / timeout** — retryable failure
- **Rate limit (429)** — verify backoff
- **AI Agent output malformed** — parser failure path (if AI used)
- **Error Trigger fires** — break a credential and confirm the error workflow receives it

### 3. Staging vs Production

- Keep a `dev` copy of the workflow with sandbox credentials.
- Use workflow **tags** (`dev`, `staging`, `prod`) and clearly prefix workflow names.
- Environment variables differ per environment — document both sets in `getting-started.md`.

## Reliability Patterns

### Idempotency

For any external write (POST/PUT/PATCH/DELETE, DB insert, message send), include an idempotency mechanism:

- Deterministic idempotency key in the request header or body (e.g., `Idempotency-Key: {{ $json.eventId }}`)
- Upsert semantics instead of insert (where the target supports it)
- Pre-check existence before write when no other option

Document the chosen mechanism in the node's `notes`.

### Retry with Backoff

Per-node retry fields:

```json
"retryOnFail": true,
"maxTries": 5,
"waitBetweenTries": 2000
```

For exponential backoff, combine with a `Wait` node in a loop controlled by `Split In Batches` or a counter in `Set`.

### Dead-Letter Pattern

When retries exhaust:

1. Route failed item to a branch that persists it (DB table, S3, another workflow queue).
2. Include the original payload, the failing node, the error message, and a timestamp.
3. Provide a replay workflow that reads the dead-letter store and re-runs the main workflow via `Execute Workflow`.

### Error Subworkflow

Standard shape of an error subworkflow:

1. `Error Trigger` — receives `{ execution, workflow, trigger }` data
2. `Set` — shape fields for alert (workflow name, node, error message, execution url)
3. `Slack` / `Email` / `PagerDuty` — notify
4. Optional: `Postgres` / `Airtable` — persist for audit and replay

Set the main workflow's `settings.errorWorkflow` to the id of this subworkflow.

### Circuit Breaker (for dependent call chains)

- Track consecutive failures in a shared store (Redis, Postgres, or n8n Static Data).
- IF count > threshold → short-circuit and route to the error branch.
- Reset on first success.

### Timeouts

- HTTP Request node: set `options.timeout` explicitly (5–30 seconds typical).
- AI Agent: set model `timeout` and agent `maxIterations`.
- Workflow-level: set `settings.executionTimeout` for long-running flows.

### Concurrency

- For Webhook triggers under load, consider queue mode on self-hosted n8n.
- For Schedule Triggers, ensure the workflow completes faster than its interval or use a lock pattern.

## Observability

- Meaningful node names (`Fetch HubSpot Contact`, not `HTTP Request2`)
- Sticky Notes at each logical section
- Workflow tags consistent with your org's conventions
- Execution data retention tuned to compliance needs — shorter for PII flows
- For critical flows, emit a heartbeat to an external monitor so silent failures are detected

## Security Checks

Before delivery, confirm:

- No secrets in `parameters`
- No secrets in `pinData`
- No secrets in node `notes`
- Webhook triggers require authentication
- User-supplied input is validated/escaped before reaching HTTP, DB, or Code nodes
- Execute Command / SSH nodes, if used, are explicitly approved and documented
