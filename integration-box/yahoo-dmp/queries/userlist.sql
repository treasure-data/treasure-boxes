SELECT
  td_global_id
FROM
  demo_pageviews
WHERE
  td_global_id IS NOT NULL
LIMIT 1000
