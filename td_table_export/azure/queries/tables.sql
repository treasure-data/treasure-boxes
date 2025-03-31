--queries/tables.sql
SELECT
  table_name AS tbl
FROM
  information_schema.tables
WHERE
  table_schema = '${td.database}'
  AND table_name LIKE 'behavior_%'