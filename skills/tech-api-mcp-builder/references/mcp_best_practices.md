# MCP Server Best Practices

## Quick Reference

### Server Naming
- **Python**: `{service}_mcp` (e.g., `slack_mcp`)
- **Node/TypeScript**: `{service}-mcp-server` (e.g., `slack-mcp-server`)

### Tool Definition Fields
- `name`: Unique identifier (1-128 chars, snake_case recommended)
- `title`: Optional human-readable display name
- `description`: Human-readable description of functionality
- `icons`: Optional array of icons for display in UIs
- `inputSchema`: JSON Schema for parameters (2020-12 dialect by default)
- `outputSchema`: Optional JSON Schema for structured output
- `annotations`: Behavioral hints (readOnlyHint, destructiveHint, etc.)

### Tool Naming
- Use snake_case with service prefix
- Format: `{service}_{action}_{resource}`
- Example: `slack_send_message`, `github_create_issue`

### Response Formats
- Support both JSON and Markdown formats
- JSON for programmatic processing
- Markdown for human readability

### Pagination
- Always respect `limit` parameter
- Return `has_more`, `next_offset`, `total_count`
- Default to 20-50 items

### Transport
- **Streamable HTTP**: For remote servers, multi-client scenarios
- **stdio**: For local integrations, command-line tools
- **HTTP+SSE**: Deprecated (protocol version 2024-11-05 only), use Streamable HTTP instead

---

## Server Naming Conventions

Follow these standardized naming patterns:

**Python**: Use format `{service}_mcp` (lowercase with underscores)
- Examples: `slack_mcp`, `github_mcp`, `jira_mcp`

**Node/TypeScript**: Use format `{service}-mcp-server` (lowercase with hyphens)
- Examples: `slack-mcp-server`, `github-mcp-server`, `jira-mcp-server`

The name should be general, descriptive of the service being integrated, easy to infer from the task description, and without version numbers.

---

## Tool Naming and Design

### Tool Naming

1. **Use snake_case**: `search_users`, `create_project`, `get_channel_info`
2. **Include service prefix**: Anticipate that your MCP server may be used alongside other MCP servers
   - Use `slack_send_message` instead of just `send_message`
   - Use `github_create_issue` instead of just `create_issue`
3. **Be action-oriented**: Start with verbs (get, list, search, create, etc.)
4. **Be specific**: Avoid generic names that could conflict with other servers

### Tool Design

- Tool descriptions must narrowly and unambiguously describe functionality
- Descriptions must precisely match actual functionality
- Provide tool annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint)
- Keep tool operations focused and atomic

---

## Response Formats

All tools that return data should support multiple formats:

### JSON Format (`response_format="json"`)
- Machine-readable structured data
- Include all available fields and metadata
- Consistent field names and types
- Use for programmatic processing

### Markdown Format (`response_format="markdown"`, typically default)
- Human-readable formatted text
- Use headers, lists, and formatting for clarity
- Convert timestamps to human-readable format
- Show display names with IDs in parentheses
- Omit verbose metadata

### Content Types in Tool Results
Tool results can include multiple content types:
- **text**: Plain text or formatted text content
- **image**: Base64-encoded image data with MIME type
- **audio**: Base64-encoded audio data with MIME type
- **resource_link**: URI reference to a resource (client can fetch on demand)
- **resource**: Embedded resource with inline content
- **structuredContent**: JSON object matching the tool's `outputSchema`

All content types support optional annotations (`audience`, `priority`, `lastModified`).

---

## Pagination

For tools that list resources:

- **Always respect the `limit` parameter**
- **Implement pagination**: Use `offset` or cursor-based pagination
- **Return pagination metadata**: Include `has_more`, `next_offset`/`next_cursor`, `total_count`
- **Never load all results into memory**: Especially important for large datasets
- **Default to reasonable limits**: 20-50 items is typical

Example pagination response:
```json
{
  "total": 150,
  "count": 20,
  "offset": 0,
  "items": [...],
  "has_more": true,
  "next_offset": 20
}
```

---

## Transport Options

### Streamable HTTP

**Best for**: Remote servers, web services, multi-client scenarios

**Characteristics**:
- Bidirectional communication over HTTP POST and GET
- Optional SSE streaming for server-to-client messages
- Supports multiple simultaneous clients
- Can be deployed as a web service
- Supports session management, resumability, and JSON-only response mode

**Requirements**:
- Clients MUST include `MCP-Protocol-Version` header on all requests after initialization
- Servers MUST validate `Origin` header to prevent DNS rebinding attacks
- Servers MUST respond with HTTP 403 Forbidden for invalid Origin headers

**Use when**:
- Serving multiple clients simultaneously
- Deploying as a cloud service
- Integration with web applications

### stdio

**Best for**: Local integrations, command-line tools

**Characteristics**:
- Standard input/output stream communication
- Simple setup, no network configuration needed
- Runs as a subprocess of the client

**Use when**:
- Building tools for local development environments
- Integrating with desktop applications
- Single-user, single-session scenarios

**Note**: stdio servers MUST NOT write anything to stdout that is not a valid MCP message. Servers MAY write UTF-8 strings to stderr for any logging purposes (informational, debug, and error messages).

### Transport Selection

| Criterion | stdio | Streamable HTTP |
|-----------|-------|-----------------|
| **Deployment** | Local | Remote |
| **Clients** | Single | Multiple |
| **Complexity** | Low | Medium |
| **Real-time** | No | Yes || **Session Mgmt** | N/A | Optional |
| **Resumability** | N/A | Optional |
---

## Security Best Practices

### Authentication and Authorization

**OAuth 2.1**:
- Use secure OAuth 2.1 with certificates from recognized authorities
- Validate access tokens before processing requests
- Only accept tokens specifically intended for your server

**API Keys**:
- Store API keys in environment variables, never in code
- Validate keys on server startup
- Provide clear error messages when authentication fails

### Input Validation

- Sanitize file paths to prevent directory traversal
- Validate URLs and external identifiers
- Check parameter sizes and ranges
- Prevent command injection in system calls
- Use schema validation (Pydantic/Zod) for all inputs

### Error Handling

- Don't expose internal errors to clients
- Log security-relevant errors server-side
- Provide helpful but not revealing error messages
- Clean up resources after errors

### DNS Rebinding Protection

For Streamable HTTP servers:
- Servers MUST validate the `Origin` header on all incoming connections
- If the `Origin` header is present and invalid, servers MUST respond with HTTP 403 Forbidden
- When running locally, servers SHOULD bind to `127.0.0.1` rather than `0.0.0.0`
- Servers SHOULD implement proper authentication for all connections

---

## Tool Annotations

Provide annotations to help clients understand tool behavior:

| Annotation | Type | Default | Description |
|-----------|------|---------|-------------|
| `readOnlyHint` | boolean | false | Tool does not modify its environment |
| `destructiveHint` | boolean | true | Tool may perform destructive updates |
| `idempotentHint` | boolean | false | Repeated calls with same args have no additional effect |
| `openWorldHint` | boolean | true | Tool interacts with external entities |

**Important**: Annotations are hints, not security guarantees. Clients MUST consider tool annotations to be untrusted unless they come from trusted servers.

### JSON Schema Dialect

MCP uses JSON Schema 2020-12 as the default dialect for `inputSchema` and `outputSchema`. If no `$schema` field is present, 2020-12 is assumed. Servers MAY specify an explicit `$schema` (e.g., `draft-07`) if needed.

---

## Error Handling

MCP uses two error reporting mechanisms:

1. **Protocol Errors**: Standard JSON-RPC errors for unknown tools, malformed requests, server errors
2. **Tool Execution Errors**: Reported in tool results with `isError: true` for API failures, input validation errors, business logic errors

**Important**: Input validation errors (e.g., wrong date format, value out of range) SHOULD be returned as Tool Execution Errors (not Protocol Errors) to enable LLM self-correction.

Guidelines:
- Provide helpful, specific error messages with suggested next steps
- Don't expose internal implementation details
- Clean up resources properly on errors

Example error handling:
```typescript
try {
  const result = performOperation();
  return { content: [{ type: "text", text: result }] };
} catch (error) {
  return {
    isError: true,
    content: [{
      type: "text",
      text: `Error: ${error.message}. Try using filter='active_only' to reduce results.`
    }]
  };
}
```

---

## Testing Requirements

Comprehensive testing should cover:

- **Functional testing**: Verify correct execution with valid/invalid inputs
- **Integration testing**: Test interaction with external systems
- **Security testing**: Validate auth, input sanitization, rate limiting
- **Performance testing**: Check behavior under load, timeouts
- **Error handling**: Ensure proper error reporting and cleanup

---

## Documentation Requirements

- Provide clear documentation of all tools and capabilities
- Include working examples (at least 3 per major feature)
- Document security considerations
- Specify required permissions and access levels
- Document rate limits and performance characteristics
