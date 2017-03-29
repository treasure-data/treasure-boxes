SELECT 
  TD_TIME_FORMAT(time,'yyyy-MM') as month,
  symbol,
  round(avg(open),2) as avg_open,
  floor(avg(volume)) as avg_vol,
  round(avg(high),2) as avg_high,
  round(avg(low),2) as avg_low,
  round(avg(close),2) as avg_close
FROM 
  nasdaq
WHERE
  TD_TIME_RANGE(time, '2014-01-01','2015-01-01') and symbol ='AAPL'
group by 1,2