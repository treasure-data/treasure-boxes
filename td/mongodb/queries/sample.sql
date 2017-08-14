SELECT 
  TD_TIME_FORMAT(time,'yyyy-MM-dd HH:mm:ss') as datetime,
  symbol,
  open,
  volume,
  high,
  low,
  close
FROM 
  nasdaq
WHERE
  TD_TIME_RANGE(time, '2014-01-01','2014-01-05')
;
