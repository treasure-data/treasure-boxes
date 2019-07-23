SELECT
  td_uid
  , MIN(exist_tduid) AS exist_tduid
  , MIN_BY(first_access_time, exist_tduid) AS first_access_time
FROM (
  SELECT
    t2.td_uid
    , t1.td_uid AS exist_tduid
    , t1.first_access_time
  FROM
    map_tduid_tdclientid AS t1
    INNER JOIN (
      SELECT
        td_client_id
        , td_uid
      FROM
        tmp_tduid_cookies
    ) AS t2 ON t1.td_client_id = t2.td_client_id
UNION ALL
  SELECT
    t2.td_uid
    , t1.td_uid AS exist_tduid
    , t1.first_access_time
  FROM
    map_tduid_tdglobalid AS t1
    INNER JOIN (
      SELECT
        td_global_id
        , td_uid
      FROM
        tmp_tduid_cookies
    ) AS t2 ON t1.td_global_id = t2.td_global_id
)
GROUP BY
  td_uid
