-- Discover all tables in cdp_lookup_catalog database
-- Excludes digest tables, temporary tables, _wf_ prefixed internal tables,
-- and tables that contain only a time column (no meaningful payload columns).
-- Note: %_digests% and %_updated% filters kept for backward compatibility with M1 tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '${td.database}'
  AND table_name NOT LIKE '%_digests%'
  AND table_name NOT LIKE '%_updated%'
  AND table_name NOT LIKE '_wf_%'
  AND table_type = 'BASE TABLE'
  AND table_name IN (
    SELECT table_name
    FROM information_schema.columns
    WHERE table_schema = '${td.database}'
      AND column_name != 'time'
  )
ORDER BY table_name
