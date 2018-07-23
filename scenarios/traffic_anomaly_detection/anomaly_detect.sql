SELECT
    CASE WHEN is_outlier = 0 THEN CONCAT("Anomaly Detected on ", TD_TIME_FORMAT(day, 'yyyy-MM-dd'), " with value of ", CAST(daily_pv AS STRING))
    ELSE ""
    END As message
FROM (
    SELECT day,
           daily_pv,
           CAST(CHANGEFINDER(daily_pv, '-outlier_threshold ${outlier_threshold}').is_outlier AS int) AS is_outlier
    FROM tmp_daily_rollup_${source_table}
    WHERE td_host = '${domain}'
    ORDER BY day
) tbl
WHERE day = TD_DATE_TRUNC('day', ${session_unixtime}-86400)
