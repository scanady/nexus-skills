# Context Log

Append-only chronological record of operations on the context repository. Each entry begins with `## [YYYY-MM-DD] <op> | <description>` so it is parseable with simple text tools.

Operations:

- `initialize` - the repository was created or configured.
- `ingest` - a source was processed into the repository.
- `query` - a question was answered against the repository, usually logged when filed back as synthesis.
- `curate` - pages, links, tags, or schema conventions were improved.
- `package` - an internal context pack was created or updated.
- `lint` - a health check was run.
- `schema` - the schema was modified.
- `shard` - an index was sharded.

---