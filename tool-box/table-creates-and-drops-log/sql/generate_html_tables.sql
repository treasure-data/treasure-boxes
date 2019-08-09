SELECT table_deletes, table_creates
FROM
  (SELECT array_join(array_agg(
    CONCAT('<tr> <td>',resource_name, '</td><td>', CAST(change_count AS varchar), '</td></tr>')), '') AS table_deletes
  FROM ${td.database}.tables_anomalous_table_drops_and_creates_last_${lookback_range_days}_days
  WHERE event_name LIKE 'table_delete'),
  (SELECT array_join(array_agg(
    CONCAT('<tr> <td>',resource_name, '</td><td>', CAST(change_count AS varchar), '</td></tr>')), '') AS table_creates
  FROM ${td.database}.tables_anomalous_table_drops_and_creates_last_${lookback_range_days}_days
  WHERE event_name LIKE 'table_create')