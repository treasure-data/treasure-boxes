SELECT table_name FROM information_schema.tables WHERE table_schema = '${td.database}'
AND table_name LIKE '${td.table_prefix}%'