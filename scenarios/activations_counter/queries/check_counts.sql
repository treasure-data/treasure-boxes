SELECT
  act_id,
  SUM(rec_cnt) AS "sum",
  COUNT(1) AS cnt
FROM
  (
  SELECT
    act_id,
    rec_cnt
  FROM
    ${td.table}
  WHERE
    act_id = ${activation_id}
  ORDER BY
    time DESC
  LIMIT 3
  )
GROUP BY
  act_id