WITH cnt_tab AS(select user_id,count(*) cnt from access_log where TD_TIME_RANGE(time, '${month}-${i}', '${month}-${i+1}', 'UTC') group by user_id),
rnk_tab AS (
SELECT 
RANK() OVER(order by cnt desc) rnk, cnt,user_id
FROM cnt_tab
)
SELECT '${month}-${i}' date,rnk,cnt,user_id FROM rnk_tab WHERE rnk <= 10
