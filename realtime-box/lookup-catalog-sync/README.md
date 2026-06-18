# Lookup Catalog Sync Workflow

Digdag workflow templates to sync tables from the `cdp_lookup_catalog` database to RT 2.0 internal storage. Only changed records are uploaded on each run (hash-based change detection).

## Variants

| Variant | When to use |
|---------|-------------|
| [manual/](./manual) | Fewer than 5 tables, schemas change infrequently, or you need explicit control over column selection. |
| [table-discovery/](./table-discovery) | 5 or more tables, schemas change frequently, or you prefer zero-maintenance automatic table detection. Requires an additional feature flag — contact Treasure AI Support. |

## Common Requirements

- A `cdp_lookup_catalog` database must exist in Data Workbench with lookup tables already created.
- Each lookup table must have its primary key as the **first column** (unique, non-null, not named `time`, type `string`/`int`/`long`).
- A TD API key must be stored in the workflow project's Secrets as `td.apikey`.
- `reactor_importer_endpoint`: see the region-specific endpoint comments in `lookup_catalog_sync.dig`.
- `reactor_instance`: provided by your Customer Success Manager or Treasure AI Support.

## Documentation

See the [Lookup Catalog Sync Workflow](https://docs.treasuredata.com/products/customer-data-platform/real-time/lookup-catalog-workflow) page in the Treasure AI documentation portal for full setup instructions, scheduling recommendations, and troubleshooting.
