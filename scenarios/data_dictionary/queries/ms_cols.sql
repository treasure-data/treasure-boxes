--queries/ms_cols.sql
SELECT
  "column" AS Column,
  column_alias AS Alias,
  "type" AS "Data Type",
  comment AS Comment
FROM
  ${temp_db}.${temp_schema_tbl}
WHERE
  "database" = '${td.each.db}'
  AND "table" = '${td.each.tbl}'