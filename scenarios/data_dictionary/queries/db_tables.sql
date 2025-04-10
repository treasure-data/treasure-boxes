--queries/db_tables.sql
SELECT
  table_name,
  SUBSTR(TO_BASE64(SHA256(CAST(table_name AS VARBINARY))), 1, 25) AS dname -- MS xlsx sheet name limitation (hash match)
FROM
  information_schema.tables
WHERE
  table_schema = '${td.database}'
ORDER BY
  table_name ASC
