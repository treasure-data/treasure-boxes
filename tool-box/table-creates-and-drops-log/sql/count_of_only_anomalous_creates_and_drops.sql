SELECT 
  event_name, 
  a.resource_name, 
  count(1) AS change_count
FROM td_audit_log.access AS a
LEFT JOIN 
  (SELECT 
    CONCAT(table_schema, '.', table_name) AS resource_name, 
    1 AS exclude
   FROM information_schema.tables
   WHERE table_schema = ANY (VALUES ${exclude_databases})
  ) AS b      
ON a.resource_name = b.resource_name      
WHERE (event_name LIKE 'table_create' OR event_name LIKE 'table_delete') 
  AND time > TO_UNIXTIME(date_trunc('day',now()))-(86400*30)
  AND a.resource_name <> ANY (VALUES ${exclude_tables})
  AND exclude IS NULL
GROUP BY event_name, a.resource_name
HAVING count(1) <= 2