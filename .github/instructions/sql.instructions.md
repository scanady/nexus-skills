---
applyTo: "**/*.sql"
---
# SQL Backend Guidelines

## Flyway Migration Checksum Management

### Dev Seed Data (V999__seed_dev_data.sql)

The `V999__seed_dev_data.sql` migration is special - it contains development test data that may be modified during development. Unlike production migrations, this file is expected to change.

**When modifying V999__seed_dev_data.sql, you MUST:**

1. **Delete the existing Flyway history record** before restarting the backend:
   ```powershell
   $env:DOCKER_HOST = "tcp://127.0.0.1:2375"
   docker exec nexus-postgres psql -U nexus -d nexuscoach -c "DELETE FROM flyway_schema_history WHERE version = '999';"
   ```

2. **Restart the backend** to reapply the migration:
   ```powershell
   .\scripts\backend-server.ps1 restart -Background
   ```

**Why this is necessary:** Flyway validates migration checksums. If a migration file is modified after being applied, Flyway will reject the change with "Migration checksum mismatch". For dev seed data, we simply delete the history record and let it reapply.

### Production Migrations (V001-V998)

**NEVER modify production migrations after they have been applied.** These are immutable. If you need to change the schema:
1. Create a new migration with the next version number
2. Add ALTER TABLE, UPDATE, or other SQL to make the change

### Migration Naming Conventions

- `V{version}__{description}.sql` - Versioned migrations (run once, in order)
- `R__{description}.sql` - Repeatable migrations (run when checksum changes)

### Common Patterns

**Adding a new column with default:**
```sql
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);
UPDATE users SET display_name = first_name || ' ' || last_name WHERE display_name IS NULL;
```

**Safe column rename (two-step):**
```sql
-- Migration N: Add new column, copy data
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
UPDATE users SET full_name = display_name;

-- Migration N+1 (after code deploys): Drop old column
ALTER TABLE users DROP COLUMN display_name;
```

## Data Seeding Best Practices

### UUID Format Requirements
**UUIDs must only contain hexadecimal characters (0-9, a-f).** Do not use letters g-z in UUID prefixes. For example, `a0000000-...` and `ed000000-...` are valid, but `sp000000-...` is not.

### Use ON CONFLICT for Idempotency
```sql
INSERT INTO users (id, email, first_name, last_name)
VALUES ('uuid', 'email@example.com', 'First', 'Last')
ON CONFLICT (id) DO NOTHING;
```

### Nullable vs Required Fields
- Use `NULL` for optional fields that should test fallback logic
- Only populate `display_name` when testing the "has display name" path
- Ensure `first_name` and `last_name` are always populated for fallback

### Testing Display Name Fallback
When seeding users, intentionally leave `display_name` as `NULL` for most records:
```sql
-- User with display_name (tests direct path)
('id1', 'user1@example.com', 'John', 'Doe', 'John Doe', ...)

-- User without display_name (tests firstName + lastName fallback)
('id2', 'user2@example.com', 'Jane', 'Smith', NULL, ...)
```
