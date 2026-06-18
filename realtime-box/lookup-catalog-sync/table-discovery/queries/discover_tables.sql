-- Discover all eligible tables in cdp_lookup_catalog.
-- Excludes internal workflow tables (_wf_* prefix).
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '${td.database}'
  AND table_name NOT LIKE '_wf_%'
  AND table_type = 'BASE TABLE'
ORDER BY table_name
