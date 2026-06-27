-- Discover all tables in cdp_lookup_catalog database
-- Excludes digest tables, temporary tables, and _wf_ prefixed internal tables
-- Note: %_digests% and %_updated% filters kept for backward compatibility with M1 tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '${td.database}'
  AND table_name NOT LIKE '%_digests%'
  AND table_name NOT LIKE '%_updated%'
  AND table_name NOT LIKE '_wf_%'
  AND table_type = 'BASE TABLE'
ORDER BY table_name
