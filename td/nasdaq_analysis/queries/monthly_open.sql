SELECT 
	TD_DATE_TRUNC('month', time), 
	AVG(daily_avg_open) AS monthly_avg_open, 
	AVG(daily_avg_close) AS month_avg_close
FROM 
	daily_open
WHERE
	TD_TIME_RANGE(time, '2013-01-01','2015-01-01')
GROUP BY 
	1