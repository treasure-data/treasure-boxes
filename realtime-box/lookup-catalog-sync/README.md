# Lookup Catalog Sync Workflow

Digdag workflow template to sync tables from the `cdp_lookup_catalog` database to RT 2.0 internal storage. Only changed records are uploaded on each run (hash-based change detection).

## Requirements

- A `cdp_lookup_catalog` database must exist in Data Workbench with lookup tables already created.
- Each lookup table must have its primary key as the **first column** (unique, non-null, not named `time`, type `string`/`int`/`long`).
- A TD API key must be stored in the workflow project's Secrets as `td.apikey`.
- `reactor_importer_endpoint`: see the region-specific endpoint comments in `lookup_catalog_sync.dig`.
- `reactor_instance`: provided by your Customer Success Manager or Treasure AI Support.

## Documentation

See the [Lookup Catalog Sync Workflow](https://docs.treasuredata.com/products/customer-data-platform/real-time/lookup-catalog-workflow) page in the Treasure AI documentation portal for full setup instructions, scheduling recommendations, and troubleshooting.
