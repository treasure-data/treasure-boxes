# Lookup Catalog Sync — Table Discovery

Use this variant when you manage many tables or want the workflow to automatically detect new tables added to `cdp_lookup_catalog`.

**Requires an additional feature flag.** Contact Treasure AI Support to enable it before using this variant.

## Setup

1. Copy this directory into your TD Workflow project.
2. Edit `lookup_catalog_sync.dig`:
   - Set `reactor_importer_endpoint` (obtain from Treasure AI Support).
   - Set `reactor_instance` (obtain from Treasure AI Support).
3. Store your TD API key in Secrets as `td.apikey`.
4. Set a schedule and run once manually to verify the initial upload.

## Files

| File | Description |
|------|-------------|
| `lookup_catalog_sync.dig` | Main workflow — discovers and syncs all tables automatically |
| `sync_table.dig` | Reusable single-table sync logic called by the main workflow |
| `scripts/generate_sql.py` | Python script that generates type-aware extract SQL per table |
| `queries/discover_tables.sql` | Discovers eligible tables, excludes `_wf_*` internal tables |
