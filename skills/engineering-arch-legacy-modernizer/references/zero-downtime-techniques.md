# Zero-Downtime Techniques

Load when a phase must change a live system with no write freeze: schema change, data move, traffic shift, or environment switch. Pair with `strangler-fig-pattern.md` for routing and `migration-strategies.md` for per-layer strategy.

## Contents

1. [Rules that make a change safe](#1-rules-that-make-a-change-safe)
2. [Schema changes without a lock](#2-schema-changes-without-a-lock)
3. [Moving data while it changes](#3-moving-data-while-it-changes)
4. [Shifting traffic](#4-shifting-traffic)
5. [Connections, sessions, and in-flight work](#5-connections-sessions-and-in-flight-work)
6. [Guardrails and automatic rollback](#6-guardrails-and-automatic-rollback)
7. [Pitfalls](#7-pitfalls)

## 1. Rules that make a change safe

1. **Two versions always overlap.** During any deploy, old and new code run at the same time against the same data. Every release must work with the schema one step ahead and one step behind.
2. **One direction per release.** A release adds, or it removes. It never does both. Adds ship first (expand). Removes ship last (contract).
3. **Switch by flag, not by deploy.** A flag flips in seconds. A deploy rollback takes minutes and can fail.
4. **Keep the old path warm until the new path is proven.** A cold old path is not a rollback. It is a rebuild.
5. **Bound every step in time.** Set `lock_timeout`, statement timeouts, and job deadlines. A step that waits forever blocks live traffic.

## 2. Schema changes without a lock

### Which DDL blocks

| Change | Risk on a busy table | Safe form |
|---|---|---|
| Add nullable column | Low. Metadata only on current PostgreSQL and MySQL 8. | Plain `ADD COLUMN`. |
| Add column with constant default | Low on PostgreSQL 11+. Rewrites the table on older versions. | Check engine version first. |
| Add `NOT NULL` | High. Full scan under lock. | Add `CHECK (col IS NOT NULL) NOT VALID`, run `VALIDATE CONSTRAINT`, then set `NOT NULL`. |
| Add index | High. Blocks writes. | `CREATE INDEX CONCURRENTLY`. |
| Add foreign key | High. Scans and locks both tables. | `ADD CONSTRAINT ... NOT VALID`, then `VALIDATE CONSTRAINT`. |
| Change column type | Highest. Rewrites the table. | New column, dual write, backfill, switch, drop. |
| Rename column or table | Breaks the old version instantly. | Add new, dual write, switch reads, drop old. Never `RENAME` in place. |
| Drop column | Breaks any reader still selecting it. | Stop reads first. Drop in the contract release. |

### Session guard

Run every DDL session with a short lock wait and retry on failure. A queued `ALTER` blocks all later queries on the table, even plain reads.

```sql
SET lock_timeout = '3s';
SET statement_timeout = '15min';
ALTER TABLE orders ADD COLUMN shipping_address_id bigint;
```

```bash
# retry loop: lock_timeout turns a long wait into a fast failure
for i in 1 2 3 4 5; do psql -v ON_ERROR_STOP=1 -f add_column.sql && break; sleep $((i * 5)); done
```

### Validate a constraint in two steps

```sql
ALTER TABLE orders ADD CONSTRAINT orders_email_nn CHECK (customer_email IS NOT NULL) NOT VALID;
-- takes only a light lock; scans while writes continue
ALTER TABLE orders VALIDATE CONSTRAINT orders_email_nn;
-- PostgreSQL 12+: the validated check lets SET NOT NULL skip the scan
ALTER TABLE orders ALTER COLUMN customer_email SET NOT NULL;
ALTER TABLE orders DROP CONSTRAINT orders_email_nn;
```

### Online change tools

Use a shadow-table tool when the engine cannot do the change online: `gh-ost` or `pt-online-schema-change` for MySQL, `pg_repack` for PostgreSQL bloat. Each tool copies rows to a shadow table, replays changes, then swaps names. Limit: plan for 2x disk, watch replica lag, and use the tool's throttle on replica lag and load. Test the cut-over swap on a copy first because it takes a brief metadata lock.

### Expand and contract, step by step

Example: split `orders.address` (text) into `addresses` rows referenced by `orders.shipping_address_id`.

| Release | Schema | Application | Rollback |
|---|---|---|---|
| 1. Expand | Add `addresses` table and nullable `shipping_address_id`. | No change. | Drop new objects. |
| 2. Dual write | None. | Write old and new. Read old. | Flag off. |
| 3. Backfill | None. | Same. | Pause job. |
| 4. Verify | None. | Same. Shadow-read new and compare. | Hold. |
| 5. Read new | None. | Read new. Still write both. | Flag back to old reads. |
| 6. Stop old writes | None. | Write new only. | Re-enable dual write, then re-backfill the gap. |
| 7. Contract | Drop `orders.address`. | Remove old code and flags. | Roll forward only. |

Releases 5 and 6 are separate on purpose. Release 5 is undone by a flag because the old column is still current. Release 6 is the first step where the old column goes stale.

## 3. Moving data while it changes

### Choose a method

| Method | Use when | Write freeze | Main risk |
|---|---|---|---|
| Dual write in the application | You own all writers and the change is a schema reshape. | None. | Writers you forgot. Partial failure between the two writes. |
| Change data capture (CDC) from the log | You move between engines or hosts and writers are many. | Seconds at cutover. | Lag, schema drift in the stream, ordering across tables. |
| Trigger-based sync | Engine has no log access and the table is small. | None. | Trigger cost on every write. |
| Snapshot and replay | Data is small or offline cutover is allowed. | Whole copy time. | Window length grows with data. |

### Dual write without lost updates

Dual write fails when the second write fails after the first commits. Handle it deliberately.

1. Write old first. Old is the source of truth until the read switch.
2. Write new second. On failure, log the key to a repair queue and continue. Do not fail the user request.
3. A repair worker re-reads the old row and upserts the new row. The repair is idempotent.
4. Alert when the repair queue age exceeds the soak limit.

```python
def save_order(order):
    legacy_repo.save(order)                    # source of truth
    if flags.on("orders.dual_write", order.customer_id):
        try:
            new_repo.upsert(to_new_shape(order))
        except Exception as exc:               # never fail the request for the secondary
            repair_queue.put(order.id)
            metrics.incr("orders.dual_write.failed")
            log.warning("dual write failed", order_id=order.id, error=str(exc))
```

Do not use a distributed transaction to remove this gap. It couples both stores' availability and hides the same race behind a coordinator. Repair plus reconciliation is cheaper and safer.

### Backfill rules

- Key batches by primary-key range, not `OFFSET`. `OFFSET` slows as it grows and skips rows under concurrent writes.
- Use upsert, so a batch can run twice with the same result.
- Compare `updated_at` or a version column, so the backfill never overwrites a newer dual-written row.
- Throttle: pause when replica lag or primary CPU passes a limit. Run in the low-traffic window.
- Checkpoint the last completed key. A crash resumes there.

```sql
-- one batch; run in a loop until no rows are returned
INSERT INTO orders_new (id, total_cents, version)
SELECT id, total_cents, version FROM orders
WHERE id > :last_id ORDER BY id LIMIT 5000
ON CONFLICT (id) DO UPDATE
   SET total_cents = EXCLUDED.total_cents, version = EXCLUDED.version
   WHERE orders_new.version < EXCLUDED.version;
```

### CDC cutover sequence

1. Load a consistent snapshot. Record the log position at snapshot time.
2. Start streaming from that position. Alert on lag.
3. Verify with lag-adjusted checks (see `data-reconciliation.md`).
4. At cutover: set the source read-only, wait for lag zero, compare final checksums, repoint, lift read-only.
5. Start reverse replication from target to source. This is the live rollback path.
6. Reset sequences on the target above the source maximum, or ids collide on the first insert.

The write freeze in step 4 is the only downtime. Rehearse it and time it. A bounded freeze of seconds to a few minutes is the honest cost of changing engines. If the budget is truly zero, use dual write.

## 4. Shifting traffic

### Pick the shift

| Shift | Rollback speed | Cost | Best for |
|---|---|---|---|
| Blue-green | Seconds (flip back) | 2x infrastructure during overlap | Stateless services, infrastructure moves. |
| Canary | Seconds (route to 0%) | Small | Service replacement with real-traffic proof. |
| Rolling | Minutes | None | Routine releases of backward-compatible code. |
| Shadow (mirror) | Not applicable. No user impact. | Duplicate load | Proving a replacement before it serves anyone. |
| Parallel run | Instant (legacy is the answer) | Duplicate load and compare cost | Replacing logic where correctness is hard to specify. |

### Canary ramp

- Select cohorts by stable hash of a user or account id. A user must not flip between versions between requests.
- Ramp 1%, 5%, 25%, 50%, 100%. Hold each step for at least one full traffic cycle (a day if usage is daily).
- Compare the canary against the control group at the same time, not against last week.
- Gate each step on the guardrails in section 6. Automate the gate.

### Weighted routing example

```yaml
# gateway route: weights are the only thing that changes per step
routes:
  - match: { path_prefix: /orders }
    split:
      - { backend: orders-legacy, weight: 95 }
      - { backend: orders-new,    weight: 5,  sticky_by: account_id }
```

### Blue-green cautions

- The database is the shared part. Blue and green must both work with the current schema, or the switch cannot be reversed.
- Lower DNS TTL to 60 seconds a full old-TTL period before the switch. Some clients ignore TTL, so keep blue serving until its traffic is near zero.
- Keep blue running and synced for the soak window. A flip back to a stale blue loses writes.

### Shadow traffic cautions

- Strip side effects. The shadow call must not send email, charge cards, or write to shared stores.
- Compare normalized output. Ignore ids, timestamps, and ordering the contract does not guarantee.
- Cap mirrored load. The mirror can overload the new service and hide real defects behind noise.

## 5. Connections, sessions, and in-flight work

| Concern | Technique |
|---|---|
| Open connections at switch | Drain: stop new connections to the old backend, let in-flight finish, set a hard deadline (30-60 s), then close. |
| Sticky sessions | Keep session state outside the process (shared store) before the shift. Otherwise users lose carts at the flip. |
| Long jobs and queues | Let the old consumers finish their messages. Start new consumers on a new queue or consumer group. Never run old and new consumers on one queue unless the handlers are idempotent. |
| Scheduled jobs | Run on exactly one side. Use a lock or a flag per job. Two cron copies double every email. |
| Caches | Version cache keys by schema or contract. A new reader on an old cached shape is a common silent failure. |
| Idempotency | Give every write a key. Retries during a flip must not apply twice. |
| Readiness | Send traffic only after a readiness probe passes against real dependencies. Keep liveness separate so a slow start does not cause a restart loop. |

## 6. Guardrails and automatic rollback

Define the guardrails before the first step, and wire them to the flag or router.

| Signal | Example limit | Window |
|---|---|---|
| Error rate vs control | +50% relative, or +0.5 points absolute | 5 min |
| p95 latency vs control | +25% | 5 min |
| Saturation (CPU, pool, replica lag) | Above the agreed ceiling | 5 min |
| Business KPI (orders, sign-ins) | -3% vs control | 1 traffic cycle |
| Data check (reconciliation diff) | Any unexplained diff in a critical table | Per run |

Rules:
- Automatic triggers cover technical signals. A human decides for business KPIs and data checks.
- A rollback trigger needs a minimum sample size. A 1% canary at low volume can trip on three errors. Require both a rate and a count.
- Tie the trigger to the exact switch that undoes the phase. If no switch exists, the phase has no rollback and must be marked roll-forward-only.
- Test the trigger. Inject a fault in staging and watch the rollback fire.

Circuit breaker fallback for a replaced dependency:

```python
class Breaker:
    """Open after N failures; send traffic to legacy until a probe succeeds."""
    def __init__(self, threshold=5, cool_off_s=60):
        self.threshold, self.cool_off_s = threshold, cool_off_s
        self.failures, self.opened_at = 0, None

    def call(self, new, legacy, *args):
        if self.opened_at and time.monotonic() - self.opened_at < self.cool_off_s:
            return legacy(*args)
        try:
            result = new(*args)
            self.failures, self.opened_at = 0, None
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold:
                self.opened_at = time.monotonic()
            return legacy(*args)
```

A breaker hides failures from users, so also emit a metric on every fallback. A silent fallback can run for weeks and the migration never actually completes.

## 7. Pitfalls

- **Dropping in the same release as the last reader's removal.** Old pods still run during the deploy. Drop one release later.
- **Backfill that overwrites newer data.** Guard with a version or timestamp comparison.
- **Sequences not reset after a cutover.** The first insert fails on a duplicate key.
- **A rollback that was never run.** Treat an unrehearsed rollback as absent.
- **Flags that never get removed.** Remove each flag in the contract release. A flag that stays becomes a permanent behavior toggle.
- **Testing only the happy cohort.** Include the oldest accounts, the largest accounts, and rows with NULLs and odd encodings in the verify and canary sets.
- **Ignoring non-HTTP consumers.** Batch jobs, BI tools, exports, and webhooks read the old shape too. Find them in access logs before contract.
