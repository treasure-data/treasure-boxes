SELECT
  time
  , td_uid
  , device_category
  , device_detail
  , device_browser
  , TD_TIME_FORMAT(start_date, 'yyyy-MM-dd', 'JST') AS access_date
  , td_session_id
  , utm_medium||' / '||utm_source AS referral
  , td_host
  , td_path
FROM
  trs_td_session
WHERE
  TD_INTERVAL(time, '${jd.target_span}')
  AND REGEXP_LIKE(td_host, '^(${jd.target_host.join("|")})$')
