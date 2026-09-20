# Lab 05 — Incremental Load: SCD Type 1 vs 2

Slowly Changing Dimensions: overwrite (type 1) vs versioned history (type 2), plus batch tracking (`stg_loaded`) making reloads idempotent. SQLite demo via stdlib; Postgres DDL in `scd.sql`.

## 1. Theory

- **SCD Type 1 (overwrite):** `UPDATE dim SET city = new` — simple, one row per entity, but history is destroyed. Right for corrections (typos) where the past must read as the present.
- **SCD Type 2 (versioning):** never update — close the current version (`valid_to = today, is_current = 0`) and insert a new one (`valid_from = today, is_current = 1`, new surrogate key). Facts keep pointing at the version that was current at event time, so old reports don't change. Costs rows; needs a `v_dim_customer_current` view for "latest" queries and a point-in-time predicate for history.
- **Incremental load:** `stg_loaded(batch)` records applied batches; the loader skips known batches → replays are no-ops. Combined with Type 2 "close + open only on change", unchanged rows cost one `SELECT`, not a rewrite.
- **Surrogate key payoff:** facts reference `customer_key` (the version), not `customer_id` (the entity) — that's what makes two "Ada" rows coexist.

## 2. Project layout

```
lab-05-incremental-load/
  scd.sql   # Postgres DDL: type-1 table, type-2 table + current view + point-in-time query
  scd.py    # runnable demo: day1/day2 loads, replay idempotency, point-in-time query
```

## 3. Run

```bash
cd lab-05-incremental-load
python3 scd.py
psql postgresql://nndsk:nndsk@localhost:5432/nndsk -f scd.sql   # needs docker compose up -d (same image as lab-01)
```

## 4. Verify

1. `python3 -m py_compile scd.py` passes; `python3 scd.py` shows SCD1 with 2 rows (Ada=Prague only) and SCD2 with 3 rows (Ada twice, old `is_current=0`).
2. Replaying day 2 changes nothing (batch guard) — row counts stable across runs (in-memory, so re-execution replays the whole script deterministically).
3. Point-in-time line prints `Pardubice` for Ada on 2026-09-01 (history query works).

## 5. Tasks

1. Add SCD Type 3 (previous-value column `prev_city`): implement in `scd.py`, show it keeps exactly one history step, and note when that's enough.
2. Handle deletes: add `is_deleted` flag handling in `load_scd2` for a customer missing from day 2.
3. Late-arriving fact: insert a fact dated 2026-09-01 for Ada after day 2 — which `customer_key` must it reference? Resolve programmatically.
4. Port `scd.py` logic to `MERGE`-based Postgres SQL (single statement per batch) and compare line counts.
