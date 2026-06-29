# Realtime Box

Workflow templates for **Treasure AI RT 2.0** features.

---

## Lookup Catalog Sync

Treasure Workflow template to sync tables from the `cdp_lookup_catalog` database to RT 2.0 internal storage. Only changed records are uploaded on each run (hash-based change detection).

### How it works

Each run follows three phases:

1. **Init** — For every discovered table, creates a `_wf_<table>_digests` table (if not exists) to track which rows have already been uploaded and their payload hash.
2. **Extract** — Generates type-aware SQL to build a `_wf_<table>_updated` staging table containing only rows whose payload hash differs from the digest.
3. **Upload & update** — If there are changed rows, uploads them to RT 2.0 via the bulk-load API, then writes the new hashes back to the digest table. Cleans up the staging table regardless.

On the first run all rows are uploaded. Subsequent runs upload only rows that were added or changed.

### Files

| File | Description |
|------|-------------|
| `lookup-catalog-sync/lookup_catalog_sync.dig` | Main workflow |
| `lookup-catalog-sync/scripts.py` | Generates type-aware JSON payload SQL per table |
| `lookup-catalog-sync/queries/discover_tables.sql` | Discovers eligible tables in `cdp_lookup_catalog` |

### Requirements

- A `cdp_lookup_catalog` database must exist in Data Workbench with lookup tables already created.
- Each lookup table must have its primary key as the **first column** (unique, non-null, not named `time`, and must be **String type**).
- A TD API key must be stored in the workflow project's Secrets as `td.apikey`.

### Setup

1. Copy the `lookup-catalog-sync/` directory into your TD Workflow project.
2. Edit `lookup_catalog_sync.dig` and set the following parameters:

| Parameter | Description |
|-----------|-------------|
| `reactor_importer_endpoint` | Region-specific endpoint (see comments in the `.dig` file) |
| `reactor_instance` | Provided by your Customer Success Manager or Treasure AI Support |
| `p_table_name` | Leave empty to sync all tables. Set to a table name to sync a single table (useful for testing). |
| `batch_size` | Number of rows per upload request (default: `1000`) |
| `parallelism` | Number of parallel upload connections (default: `10`) |

3. Store your TD API key in Secrets as `td.apikey`.
4. Schedule the workflow (daily recommended) and run once manually to verify the initial full upload.

### Supported column types

`scripts.py` generates a JSON `payload` string for each row with the following type handling:

| TD column type | JSON serialization |
|----------------|--------------------|
| `varchar`, `integer`, `bigint`, etc. | String with quote escaping; numeric values serialized without quotes |
| `double`, `real` | Trailing-zero stripped decimal (e.g. `1.5` not `1.500000`) |
| `array(varchar)` | JSON array of strings with NULL element preservation |
| `array(bigint)`, `array(integer)` | JSON array of integers |
| `array(double)`, `array(real)` | JSON array of trailing-zero stripped decimals |
| Other `array(*)` types | Raises an error — flatten the column before ingestion |

The key column (first column) and `time` are excluded from the payload.

### Documentation

See the [Lookup Catalog Sync Workflow](https://docs.treasuredata.com/products/customer-data-platform/real-time/lookup-catalog-workflow) page in the Treasure AI documentation portal for full setup instructions, scheduling recommendations, and troubleshooting.

### Error Handling

#### Invalid JSON Payload

The bulk-load API endpoint validates each record's JSON payload before ingestion. Records containing malformed JSON are rejected with an HTTP 400 Bad Request response.

Common causes:

1. Unescaped double quotes within string values
2. Trailing or missing commas
3. Mismatched or extra braces/brackets

Error response format:

```json
{
  "errorMessage": "Downstream service returned status: 400. Response: {\"statusCode\":400,\"body\":\"{\\\"message\\\":\\\"Invalid JSON data for key <record_key>: SyntaxError: <parse_error_detail>\\\"}\"}'"
}
```

If this error occurs, inspect the source table for values that contain special characters (e.g. double quotes, backslashes) and ensure they are properly escaped before ingestion.
