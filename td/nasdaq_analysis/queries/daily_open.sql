SELECT 
	TD_DATE_TRUNC('day', time), AVG(open) AS daily_avg_open, AVG(close) AS daily_avg_close
FROM 
	sample_datasets.nasdaq
WHERE
	TD_TIME_RANGE(time, '2013-01-01','2015-01-01')
GROUP BY 
	1
