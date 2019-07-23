WITH log AS (
  SELECT
    td_uid
    , MIN_BY(td_user_agent, IF(td_user_agent IS NULL, 99999999999, access_time)) AS td_user_agent
  FROM
    tmp_incr_trs_session
  GROUP BY
    td_uid
)

SELECT
  td_uid
  , REGEXP_REPLACE(COALESCE(TD_PARSE_AGENT(td_user_agent)['category'], 'unknown'), 'UNKNOWN', 'unknown') AS device_category
  , REGEXP_REPLACE(COALESCE(TD_PARSE_AGENT(td_user_agent)['os'], 'unknown'), 'UNKNOWN', 'unknown') AS device_detail
  , REGEXP_REPLACE(COALESCE(TD_PARSE_AGENT(td_user_agent)['name'], 'unknown'), 'UNKNOWN', 'unknown') AS device_browser
FROM
  log
