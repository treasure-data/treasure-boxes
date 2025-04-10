--queries/ms_tables.sql
SELECT
  "database" AS db,
  "table" AS tbl
FROM
  ${temp_db}.${temp_schema_tbl}
GROUP BY
  "database",
  "table"
