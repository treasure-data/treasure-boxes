-- set session distributed_join = 'true'
WITH log_all AS (
  SELECT
    ${type}_session_id
    , TD_IP_TO_COUNTRY_NAME(td_ip) AS country_name
    , TD_IP_TO_LEAST_SPECIFIC_SUBDIVISION_NAME(td_ip) AS prefecture_name
    , TD_IP_TO_CITY_NAME(td_ip) AS city_name
    , COALESCE(REGEXP_EXTRACT(referrer_param, '(^|&)(q|searchfor|MT|query|Text|p|qt)=([^&]+)(&|$)', 3), '(not provided)') AS organic_search_kw
  FROM (
    SELECT
      ${type}_session_id
      , SPLIT_PART(REGEXP_REPLACE(td_ip, '^,', ''), ',', 1) AS td_ip
      , URL_EXTRACT_QUERY(td_referrer) AS referrer_param
    FROM
      tmp_incr_trs_session
    WHERE
      ${type}_row_num = 1
  )
)

SELECT
  t1.${type}_session_id
  , t1.country_name
  , REGEXP_REPLACE(REGEXP_REPLACE(t1.prefecture_name, '^Ō', 'O'), 'ō', 'o') AS prefecture_name
  , REGEXP_REPLACE(REGEXP_REPLACE(t1.city_name, '^Ō', 'O'), 'ō', 'o') AS city_name
  , t2.referral_source
  , t2.utm_source
  , t2.utm_medium
  , t2.utm_campaign
  , t2.utm_content
  , t2.utm_term
  , IF(t2.utm_medium = 'organic', t1.organic_search_kw, NULL) AS organic_search_kw
FROM
  log_all AS t1
  LEFT JOIN tmp_mst_${type}_session_id_step1 AS t2 ON t1.${type}_session_id = t2.${type}_session_id
