-- set session distributed_join = 'true'
WITH t0 AS (
SELECT
c0 AS tapad_cluster_id,
split(c1,chr(9)) AS other_ids
FROM ${td.dga_tbl}
WHERE TD_TIME_RANGE(time, TD_TIME_ADD(TD_SCHEDULED_TIME(),'-1d','JST'), NULL, 'JST')
),

t1 AS (
SELECT
tapad_cluster_id,
split(other_id,'=') AS other_id
FROM t0
CROSS JOIN UNNEST (other_ids) AS t(other_id)
),

t2 AS (
SELECT
tapad_cluster_id,
CASE element_at(other_id, 1) WHEN '${tapad.cookie_prefix}' THEN element_at(other_id, 2) END AS td_cookie,
CASE element_at(other_id, 1) WHEN 'HARDWARE_MD5IDFA'       THEN element_at(other_id, 2) END AS tapad_md5_idfa,
CASE element_at(other_id, 1) WHEN 'HARDWARE_SHA1IDFA'      THEN element_at(other_id, 2) END AS tapad_sha1_idfa,
CASE element_at(other_id, 1) WHEN 'HARDWARE_ANDROID_AD_ID' THEN element_at(other_id, 2) END AS tapad_adid,
CASE element_at(other_id, 1) WHEN 'HARDWARE_IDFA'          THEN element_at(other_id, 2) END AS tapad_idfa
FROM t1
)

SELECT
tapad_cluster_id,
array_agg(td_cookie)       AS td_cookie,
array_agg(tapad_md5_idfa)  AS tapad_md5_idfa,
array_agg(tapad_sha1_idfa) AS tapad_sha1_idfa,
array_agg(tapad_adid)      AS tapad_adid,
array_agg(tapad_idfa)      AS tapad_idfa
FROM t2
GROUP BY 1
