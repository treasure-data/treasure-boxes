WITH a AS (
SELECT cookie, tapad_adid
FROM ${td.id_map_tbl}
CROSS JOIN UNNEST(td_cookie) AS t(cookie)
WHERE tapad_adid is not NULL
AND TD_TIME_RANGE(time, TD_TIME_ADD(TD_SCHEDULED_TIME(),'-1d','JST'), NULL, 'JST')
)
SELECT cookie, adid
FROM a
CROSS JOIN UNNEST(tapad_adid) AS t(adid)
GROUP BY 1,2
