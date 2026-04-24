# n8n Workflow JSON Schema

Reference for the exact structure of an importable n8n workflow JSON. Load before writing or validating JSON (Step 3 / Step 5).

## Top-Level Structure

```json
{
  "name": "human-readable workflow name",
  "nodes": [ /* array of node objects */ ],
  "connections": { /* keyed by SOURCE NODE NAME */ },
  "active": false,
  "settings": {
    "executionOrder": "v1",
    "saveManualExecutions": true,
    "callerPolicy": "workflowsFromSameOwner",
    "errorWorkflow": "<optional: id of error subworkflow>"
  },
  "pinData": {},
  "meta": {
    "templateCredsSetupCompleted": false
  },
  "versionId": "<uuidv4>"
}
```

Required fields for import: `name`, `nodes`, `connections`. Everything else has sensible defaults but SHOULD be included.

**Always export with `active: false`.** The user activates it manually after reviewing.

## Node Object

```json
{
  "id": "<uuidv4>",
  "name": "Unique Node Name",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [460, 300],
  "parameters": { /* node-type-specific */ },
  "credentials": {
    "httpBasicAuth": {
      "id": "<credential-id-placeholder>",
      "name": "My HTTP Basic Auth"
    }
  },
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 2000,
  "continueOnFail": false,
  "notes": "Short description of what this node does",
  "notesInFlow": true,
  "disabled": false
}
```

Rules:

- `id` — UUIDv4, unique across the workflow.
- `name` — unique across the workflow; connections reference this, not the id.
- `type` — fully-qualified node type. Base nodes: `n8n-nodes-base.<nodeName>`. LangChain nodes: `@n8n/n8n-nodes-langchain.<nodeName>`.
- `typeVersion` — required; matches the node's current version. When unsure, state the assumption in design summary and let the user adjust on import.
- `position` — `[x, y]`; grid-align on 20px units. Layout trigger on the far left (≈ x=250), main flow left-to-right in ~220px increments, error branch below main (y +300).
- `parameters` — shape depends on node type. Reference n8n docs for each node.
- `credentials` — include an object keyed by credential type with `id` as a placeholder string and a readable `name`. User replaces on import.
- Error/retry fields: `retryOnFail`, `maxTries`, `waitBetweenTries`, `continueOnFail` — set on every external-call node.

## Connections Object

Keyed by **source node NAME** (not id):

```json
{
  "Webhook": {
    "main": [
      [
        { "node": "Validate Input", "type": "main", "index": 0 }
      ]
    ]
  },
  "Validate Input": {
    "main": [
      [
        { "node": "Fetch Data", "type": "main", "index": 0 }
      ]
    ]
  }
}
```

Structure: `connections[sourceName][outputType][outputIndex] = [ { node, type, index }, ... ]`

- `outputType` is usually `"main"`. AI Agent tool/memory connections use `"ai_tool"`, `"ai_memory"`, `"ai_languageModel"`, `"ai_outputParser"`.
- `outputIndex` lets IF/Switch route to different downstreams: IF has indexes 0 (true) and 1 (false); Switch has one per rule.
- Multiple destinations from the same output = multiple entries in the inner array (parallel fan-out).

## Sticky Note

```json
{
  "id": "<uuidv4>",
  "name": "Sticky Note",
  "type": "n8n-nodes-base.stickyNote",
  "typeVersion": 1,
  "position": [200, 100],
  "parameters": {
    "content": "## Workflow Purpose\n\n...",
    "height": 200,
    "width": 400,
    "color": 5
  }
}
```

Sticky notes have **no connections**. Place one at the top of the workflow summarizing purpose, trigger, inputs, outputs, owner.

## Common Node Types (quick reference)

| Node | Type string |
|------|-------------|
| Webhook | `n8n-nodes-base.webhook` |
| Schedule Trigger | `n8n-nodes-base.scheduleTrigger` |
| Manual Trigger | `n8n-nodes-base.manualTrigger` |
| Error Trigger | `n8n-nodes-base.errorTrigger` |
| HTTP Request | `n8n-nodes-base.httpRequest` |
| Code | `n8n-nodes-base.code` |
| IF | `n8n-nodes-base.if` |
| Switch | `n8n-nodes-base.switch` |
| Merge | `n8n-nodes-base.merge` |
| Set / Edit Fields | `n8n-nodes-base.set` |
| Split In Batches | `n8n-nodes-base.splitInBatches` |
| Wait | `n8n-nodes-base.wait` |
| Execute Workflow | `n8n-nodes-base.executeWorkflow` |
| Sticky Note | `n8n-nodes-base.stickyNote` |
| AI Agent | `@n8n/n8n-nodes-langchain.agent` |
| Chat Trigger | `@n8n/n8n-nodes-langchain.chatTrigger` |
| OpenAI Chat Model | `@n8n/n8n-nodes-langchain.lmChatOpenAi` |
| Anthropic Chat Model | `@n8n/n8n-nodes-langchain.lmChatAnthropic` |
| Window Buffer Memory | `@n8n/n8n-nodes-langchain.memoryBufferWindow` |
| Structured Output Parser | `@n8n/n8n-nodes-langchain.outputParserStructured` |
| HTTP Request Tool | `@n8n/n8n-nodes-langchain.toolHttpRequest` |

Node `typeVersion` values evolve. If unsure of current version, use the most recent known version and note the assumption.

## Expressions

- `{{ $json.fieldName }}` — current item's JSON field
- `{{ $node["Other Node"].json.field }}` — field from another node's output
- `{{ $env.VAR_NAME }}` — environment variable
- `{{ $now }}`, `{{ $today }}` — current time helpers
- `{{ $itemIndex }}`, `{{ $runIndex }}` — positional helpers

Expressions are strings wrapped in `={{ ... }}` in `parameters` values, e.g. `"url": "={{ $env.API_BASE }}/users"`.

## Validation Checklist

Before handoff:

1. `JSON.parse()` succeeds
2. Every `name` in `nodes` is unique
3. Every `id` in `nodes` is unique and a valid UUIDv4
4. Every source key in `connections` exists in `nodes`
5. Every target `node` in `connections` exists in `nodes`
6. `active` is `false`
7. No secrets embedded anywhere in `parameters`
8. Every `credentials.*.id` value is a recognizable placeholder (not a real id)
9. Every `$env.VAR` used in parameters is listed in `getting-started.md`
