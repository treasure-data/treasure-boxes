# Lookup Catalog Sync — Manual Configuration

Use this variant when you have a small number of tables and want explicit control over which columns are synced.

## Setup

1. Copy this directory into your TD Workflow project.
2. Edit `lookup_catalog_sync.dig`:
   - Set `reactor_importer_endpoint` (obtain from Treasure AI Support).
   - Set `reactor_instance` (obtain from Treasure AI Support).
   - Define each table under `tables:` with `name`, `key_column`, and `col_expr`.
3. Store your TD API key in Secrets as `td.apikey`.
4. Set a schedule and run once manually to verify the initial upload.

## Files

| File | Description |
|------|-------------|
| `lookup_catalog_sync.dig` | Main workflow — iterates over configured tables |
| `queries/initialize_digest.sql` | Creates digest tracking table if not exists |
| `queries/extract_updated.sql` | Extracts changed records by hash comparison |
| `queries/check_count.sql` | Counts changed records |
| `queries/update_digest.sql` | Updates digest table after upload |
