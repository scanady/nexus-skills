# n8n Best Practices

Reference for designing production-grade n8n workflows. Load during design (Step 2) and before emitting JSON (Step 3).

## 1. Trigger Selection

| Use case | Trigger |
|----------|---------|
| External system pushes events | **Webhook** (add HMAC/header auth) |
| Time-based job | **Schedule Trigger** (cron syntax) |
| User-submitted data | **Form Trigger** |
| Ad-hoc / human-in-the-loop | **Manual Trigger** |
| Conversational interface | **Chat Trigger** |
| Recover from failed executions | **Error Trigger** (in a dedicated error subworkflow) |
| Polling an external system | Service-specific trigger (Gmail, Slack, etc.) — prefer over HTTP polling loops |

Prefer push (webhook) over pull (polling) whenever the source supports it.

## 2. Workflow Decomposition

Split into sub-workflows via `Execute Workflow` node when any of these are true:

- Logic exceeds ~20 nodes
- Same logic is reused across multiple parent flows
- A portion of the flow has fundamentally different retry/error characteristics
- Parts need to be tested independently

Keep each workflow single-purpose. Name workflows `verb-noun-context` (e.g., `sync-hubspot-contacts`, `notify-slack-on-error`).

## 3. Error Handling

### Per-node

- `retryOnFail: true` with `maxTries: 3–5` and `waitBetweenTries: 1000–5000` ms for all external HTTP calls
- Use `continueOnFail: true` only when a downstream branch explicitly handles the failure data
- For batch operations, combine with `Split In Batches` and route failed items to a separate branch

### Workflow-level

- Every workflow with external side effects must have an **Error Trigger** subworkflow that:
  - Logs the execution id, workflow name, error message, node name
  - Posts to an alert channel (Slack/Email/PagerDuty)
  - Optionally writes to a dead-letter store (DB table, S3, or another n8n workflow) for replay

Set the main workflow's `settings.errorWorkflow` to the id of the error subworkflow.

## 4. Reliability Patterns

| Pattern | When to apply |
|---------|---------------|
| **Idempotency key** | Any external write that could be retried — include a deterministic key in the request so duplicates are safely ignored |
| **Exponential backoff** | 3rd-party APIs with rate limits — use retry + Wait node with increasing delays |
| **Dead-letter queue** | Messages that fail after max retries — persist for manual review |
| **Circuit breaker** | Chain of dependent calls — short-circuit with IF after N consecutive failures |
| **Pinned data** | Development — pin representative input on the trigger to iterate without re-triggering |
| **Sub-workflow for writes** | Isolate side-effecting operations so the parent can retry the whole block atomically |

## 5. Branching and Merging

- Use **IF** for binary decisions. Use **Switch** for 3+ routes.
- When parallel branches must rejoin, use **Merge** in `Append`, `Pass Through`, or `Combine` mode — pick deliberately.
- Avoid deep nesting — prefer flattening with `Switch` or dedicated sub-workflows.

## 6. Data Shaping

- Use **Edit Fields / Set** to make data contracts explicit between nodes — do not rely on implicit upstream shapes.
- Use **Code** (JavaScript or Python) only when no built-in node fits; document the node's input and output shape in its notes.
- For large lists, wrap with **Split In Batches** (batch size 10–100) to avoid memory pressure and allow incremental progress.

## 7. AI Agent Nodes

When using the AI Agent / LangChain nodes:

- Pick the model deliberately; state it in the design summary (e.g., `gpt-4o-mini`, `claude-sonnet-4`, local model).
- Provide a concise **system prompt** defining role, tools, and output contract.
- Attach only the **tools** the agent actually needs — over-tooling increases latency and error rates.
- Use a **Memory** node only when the workflow is conversational or multi-turn.
- Use a **Structured Output Parser** (or the agent's JSON mode) whenever downstream nodes consume the agent's output. Never parse free-form text with regex downstream.
- Set a reasonable **max iterations** (e.g., 5–10) and a timeout.
- Route parser failures to the error branch.

## 8. Security

- All secrets go through **Credentials** or `$env.VAR` — never inline.
- Webhooks: require HMAC signature, header auth, or basic auth. Validate inside the workflow with an IF + error branch.
- `Execute Command` and `SSH` nodes: disabled on n8n Cloud; on self-hosted, use only with explicit user approval and note the risk in `getting-started.md`.
- Sanitize any user-supplied input before passing to HTTP, DB, or command nodes.
- For PII/PHI flows, disable execution data retention or mask fields before storage.

## 9. Observability

- Name nodes descriptively: `Fetch HubSpot Contact`, not `HTTP Request`.
- Add **Sticky Notes** at each major section: purpose, inputs, outputs, owner.
- Tag workflows (`prod`, `billing`, `experimental`) for filtering in the UI.
- Keep execution data retention tuned to your compliance needs.

## 10. Testing

- Pin sample input on the trigger node to enable repeatable manual executions.
- Run the workflow in **manual** mode first with representative edge cases (empty list, missing field, API 429, API 500).
- For AI Agent flows, run a small suite of prompts and check output shape and content.
- Before activating, verify the Error Trigger subworkflow fires by intentionally breaking a credential.

## 11. Cloud vs Self-Hosted

Ask the user which they are on. Differences that affect design:

- **n8n Cloud**: `Execute Command` / `SSH` / arbitrary filesystem access disabled; limited concurrent executions on smaller plans; community nodes only on certain plans.
- **Self-hosted**: Full node set; user controls queue mode, workers, and concurrency.
