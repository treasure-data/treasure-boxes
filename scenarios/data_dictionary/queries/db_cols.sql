--queries/db_cols.sql
SELECT
  column_name,
  ordinal_position,
  column_default,
  is_nullable,
  data_type
FROM
  information_schema.columns
WHERE
  table_schema = '${td.database}'
  AND table_name = '${td.each.table_name}'