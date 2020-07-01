SELECT
  td_global_id        AS td_global_id,
  MAX(td_os)          AS type,
  COUNT(td_global_id) AS price
FROM
  demo_pageviews
GROUP BY td_global_id
