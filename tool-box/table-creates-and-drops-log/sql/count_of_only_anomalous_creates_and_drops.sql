SELECT 
  event_name,
  resource_name, 
  count(1) AS change_count
FROM td_audit_log.access
WHERE (event_name LIKE 'table_create' OR event_name LIKE 'table_delete') 
  AND time > TO_UNIXTIME(date_trunc('day',now()))-(86400*${anomaly_range_days})
  AND NOT regexp_like(resource_name, ${"'" + exclude_tables.join("|").replace(/,/g, ",") + "'"})
  AND NOT regexp_like(REGEXP_REPLACE(resource_name, '\..{1,}'), ${"'" + exclude_databases.join("|").replace(/,/g, ",") + "'"})
GROUP BY event_name, resource_name
HAVING count(1) <= ${anomaly_threashold}