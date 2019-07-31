SELECT 
  a.event_name, 
  a.resource_name, 
  count(1) AS change_count
FROM td_audit_log.access AS a
JOIN ${td.database}.counts_of_table_drops_and_creates_last_${anomaly_range_days}_days AS b              
ON a.resource_name = b.resource_name AND a.event_name = b.event_name
WHERE a.time > TO_UNIXTIME(date_trunc('day',now()))-(86400*${lookback_range_days})
GROUP BY a.event_name, a.resource_name