WITH key_actions AS (
  SELECT
    CAST(json_extract_scalar(action, '$.td_host') AS VARCHAR) td_host
    , CAST(json_extract_scalar(action, '$.td_path') AS VARCHAR) td_path
    , 1 AS is_key_action
  FROM (
    SELECT
      CAST(json_parse('${jd.key_action}') AS ARRAY<JSON>) actions
  ) CROSS JOIN UNNEST(actions) AS t(action)
)

SELECT
  t1.td_uid
  , t1.td_session_id
  , MIN_BY(t1.access_date, t1.time) AS access_date
  , MIN_BY(t1.referral, t1.time) AS referral
  , t1.td_host
  , COALESCE(t2.is_key_action, 0) AS is_key_action
  , ARRAY_JOIN(ARRAY_AGG(t1.td_path||' (pv:'||CAST(t1.pv AS VARCHAR)||')'), CHR(13)) AS td_path
  , SUM(t1.pv) AS pv
FROM
  tmp_journey_data_step3 AS t1
  LEFT JOIN key_actions AS t2 ON t1.td_host = t2.td_host AND t1.td_path = t2.td_path
GROUP BY
  t1.td_uid
  , t1.td_session_id
  , t1.td_host
  , COALESCE(t2.is_key_action, 0)
