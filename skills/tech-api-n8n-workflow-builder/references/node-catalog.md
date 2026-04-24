# n8n Node Catalog

Curated catalog of commonly used nodes, grouped by role. Load during node selection (Step 2).

## Triggers

| Node | When to use |
|------|-------------|
| **Webhook** | External system notifies n8n via HTTP. Configure auth (HMAC, header, basic). |
| **Schedule Trigger** | Cron-style periodic runs. |
| **Manual Trigger** | Ad-hoc or human-initiated flows. |
| **Form Trigger** | Collect structured input from a hosted n8n form. |
| **Chat Trigger** | Conversational AI flows with session memory. |
| **Error Trigger** | First node of an error-handling subworkflow; receives failed execution metadata. |
| Service triggers (Gmail, Slack, GitHub, etc.) | Prefer over HTTP polling when available. |

## Logic & Control Flow

| Node | When to use |
|------|-------------|
| **IF** | Binary split on a condition. |
| **Switch** | Multi-way split on a value (3+ routes). |
| **Merge** | Combine parallel branches. Pick mode: `Append`, `Combine (by key)`, `Pass Through`. |
| **Split In Batches** | Process a large array incrementally; supports a loop-back pattern. |
| **Wait** | Delay execution (seconds, minutes, until time, or until webhook). |
| **Stop And Error** | Fail the execution deliberately to trigger the Error workflow. |
| **Execute Workflow** | Call a sub-workflow; essential for decomposition and reuse. |
| **No Operation** | Placeholder / visual grouping. |

## Data Transformation

| Node | When to use |
|------|-------------|
| **Set / Edit Fields** | Make data contracts between nodes explicit; rename, drop, add fields. |
| **Code** | JS or Python when no built-in fits. Document IO shape in notes. |
| **Item Lists** | Aggregate, split, sort, limit items. |
| **DateTime** | Format and arithmetic on dates. |
| **Crypto** | Hashing, HMAC, encoding. |
| **Compression** | Zip/unzip binary data. |

## HTTP & Integration

| Node | When to use |
|------|-------------|
| **HTTP Request** | Generic REST calls. Use built-in auth, retry, pagination. |
| **GraphQL** | GraphQL queries with variables. |
| **Webhook Response** | Return a response to a Webhook trigger (pair them). |
| Service nodes (Slack, Discord, Gmail, HubSpot, Airtable, Notion, Google Sheets, Postgres, MySQL, MongoDB, S3, etc.) | Prefer service-specific nodes over raw HTTP when available — they handle auth, pagination, and schemas. |

## AI / LangChain

| Node | When to use |
|------|-------------|
| **AI Agent** | Tool-using LLM agent. Attach a chat model, optional memory, tools, and output parser. |
| **Chat Model** (OpenAI, Anthropic, Ollama, Google, Mistral, etc.) | LLM backing an Agent or LLM Chain. |
| **LLM Chain** | Simple prompt → completion without tool use. |
| **Structured Output Parser** | Force JSON output against a schema. Use whenever downstream nodes read the output. |
| **Window Buffer Memory** | Short-term conversation memory. |
| **Vector Store** (Pinecone, Qdrant, PGVector, Supabase, etc.) | Retrieval-augmented generation. |
| **Embeddings** | Create vectors for ingest or query. |
| **Tool nodes** (HTTP Request Tool, Workflow Tool, Code Tool, Calculator, etc.) | Give the Agent callable capabilities. Minimize tool count. |
| **Text Splitter** | Chunk documents before embedding. |
| **Document Loaders** | Load files / URLs as LangChain documents. |

## File & Binary

| Node | When to use |
|------|-------------|
| **Read/Write Binary Files** | Local file I/O (self-hosted only in most cases). |
| **Extract from File** | Parse PDF, CSV, JSON, XML from binary input. |
| **Convert to File** | Produce binary from JSON/text. |
| **HTTP Request** with `responseFormat: file` | Download remote file. |

## Cloud vs Self-Hosted Availability

- **Cloud-restricted**: `Execute Command`, `SSH`, arbitrary filesystem read/write outside the workflow storage layer.
- **Self-hosted only by default**: some community nodes, host-network integrations.

Always ask the user which environment they target if it affects node choice.

## Selection Heuristics

1. Prefer a service-specific node over `HTTP Request` when one exists — cleaner auth, pagination, and schema.
2. Prefer built-in logic nodes (IF/Switch/Merge) over `Code` for control flow.
3. Prefer `Execute Workflow` sub-workflows over mega-flows when logic exceeds ~20 nodes or repeats.
4. Prefer `Structured Output Parser` over post-hoc regex on LLM output.
5. Prefer push triggers (Webhook, service triggers) over polling.
