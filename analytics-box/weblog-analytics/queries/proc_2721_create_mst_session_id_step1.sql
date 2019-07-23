WITH cmp_ga AS (
  SELECT
    ${type}_session_id
    , 'utm_params' AS referral_source
    , COALESCE(URL_EXTRACT_PARAMETER(td_url, 'utm_source'), '') AS utm_source
    , COALESCE(URL_EXTRACT_PARAMETER(td_url, 'utm_medium'), '') AS utm_medium
    , COALESCE(URL_EXTRACT_PARAMETER(td_url, 'utm_campaign'), '') AS utm_campaign
    , COALESCE(URL_EXTRACT_PARAMETER(td_url, 'utm_content'), '') AS utm_content
    , COALESCE(URL_EXTRACT_PARAMETER(td_url, 'utm_term'), '') AS utm_term
  FROM
    tmp_incr_trs_session
  WHERE
    ${type}_row_num = 1
    AND REGEXP_LIKE(td_params, 'utm_')
)
, log_not_ga AS (
  SELECT
    ${type}_session_id
    , CASE
        WHEN referrer_host = '' OR referrer_host = td_host
          THEN '(direct)/(none)'
        WHEN REGEXP_LIKE(referrer_host, '(mail)\.(google|yahoo|nifty|excite|ocn|odn|jimdo)\.')
          THEN CONCAT(REGEXP_EXTRACT(referrer_host, '(mail)\.(google|yahoo|nifty|excite|ocn|odn|jimdo)\.', 2), '/mail')
        WHEN REGEXP_LIKE(referrer_host, '^outlook.live.com$')
          THEN 'outlook/mail'
        WHEN REGEXP_LIKE(referrer_host, '\.*(facebook|instagram|line|ameblo)\.')
          THEN CONCAT(REGEXP_EXTRACT(referrer_host, '\.*(facebook|instagram|line|ameblo)\.', 1), '/social')
        WHEN REGEXP_LIKE(referrer_host, '^t.co$')
          THEN 'twitter/social'
        WHEN REGEXP_LIKE(referrer_host, '\.(criteo|outbrain)\.')
          THEN CONCAT(REGEXP_EXTRACT(referrer_host, '\.(criteo|outbrain)\.', 1), '/display')
        WHEN REGEXP_LIKE(referrer_host, '(search)*\.*(google|yahoo|biglobe|nifty|goo|so-net|livedoor|rakuten|auone|docomo|naver|hao123|myway|dolphin-browser|fenrir|norton|uqmobile|net-lavi|newsplus|jword|ask|myjcom|1and1|excite|mysearch|kensakuplus)\.')
          THEN CONCAT(REGEXP_EXTRACT(referrer_host, '(search)*\.*(google|yahoo|biglobe|nifty|goo|so-net|livedoor|rakuten|auone|docomo|naver|hao123|myway|dolphin-browser|fenrir|norton|uqmobile|net-lavi|newsplus|jword|ask|myjcom|1and1|excite|mysearch|kensakuplus)\.', 2), '/organic')
        WHEN referrer_host = 'kids.yahoo.co.jp' AND referrer_path = 'search' THEN 'yahoo/organic'
      ELSE CONCAT(referrer_host, '/referral')
    END source_medium
  FROM (
    SELECT
      ${type}_session_id
      , td_host
      , COALESCE(URL_EXTRACT_HOST(td_referrer), '') AS referrer_host
      , SPLIT_PART(URL_EXTRACT_PATH(td_referrer), '/', 2) AS referrer_path
    FROM
      tmp_incr_trs_session
    WHERE
      ${type}_row_num = 1
      AND NOT REGEXP_LIKE(td_params, 'utm_')
  )
)
, cmp_not_ga AS (
  SELECT
    ${type}_session_id
    , 'td_referrer' AS referral_source
    , SPLIT(source_medium, '/')[1] AS utm_source
    , SPLIT(source_medium, '/')[2] AS utm_medium
    , CAST(NULL AS VARCHAR) AS utm_campaign
    , CAST(NULL AS VARCHAR) AS utm_content
    , CAST(NULL AS VARCHAR) AS utm_term
  FROM
    log_not_ga
)


SELECT
  *
FROM
  cmp_ga
UNION ALL
SELECT
  *
FROM
  cmp_not_ga
