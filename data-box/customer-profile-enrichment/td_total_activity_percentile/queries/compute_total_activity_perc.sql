WITH t1 as (
  SELECT
  row_number() over(order by COUNT(*) desc) actions_rnk,
  u.${user_master_join_key}, 
  COUNT(*) actions_total
  FROM ${activity_table} a
  LEFT JOIN ${user_master_table} u 
  ON a.${activity_table_join_key} = u.${user_master_join_key}
  GROUP BY u.${user_master_join_key}
),

t2 as (
  SELECT
  ${user_master_join_key},
  CAST((SELECT max(actions_rnk) FROM t1) as double) total_users,
  CAST(actions_rnk as double) as actions_rnk
  FROM t1
),

t3 as (
  SELECT 
  ${user_master_join_key},
  CAST(FLOOR((1 - actions_rnk / total_users) * 100) as INTEGER) as td_total_activity_perc
  FROM t2
  ORDER BY td_total_activity_perc desc
)
SELECT u.*,
(case when td_total_activity_perc >= 1 and td_total_activity_perc <= 20 then   1 
                    when  td_total_activity_perc >= 21 and td_total_activity_perc <= 40 then  2
                    when  td_total_activity_perc >= 41 and td_total_activity_perc <= 60 then  3
                    when  td_total_activity_perc >= 61 and td_total_activity_perc <= 80 then  4
                    when  td_total_activity_perc >= 81 and td_total_activity_perc <= 100 then 5
                    when  td_total_activity_perc is null then 0
                    end ) as td_total_activity_percentile
FROM ${user_master_table} u
LEFT JOIN t3 on u.${user_master_join_key} = t3.${user_master_join_key}
ORDER BY td_total_activity_perc DESC

