WITH rnk_tab AS(
SELECT
RANK() OVER(order by cnt desc) rnk, date,cnt,user_id
FROM aggregated_table
)
SELECT rnk,cnt,user_id,date FROM rnk_tab WHERE rnk <= 10
