WITH T0 AS 
(
select A.${activity_table_join_key}
from ${activity_table} A 
 where TD_TIME_RANGE(time, TD_TIME_ADD(TD_SCHEDULED_TIME(), '-42w'),TD_SCHEDULED_TIME())
),
T1
AS 
(
select A.${activity_table_join_key} ,TD_TIME_FORMAT(time,'YYYYMM') as yearmonth,count(*) as cnt
from ${activity_table} A join T0 on A.${activity_table_join_key} = T0.${activity_table_join_key}
where TD_TIME_RANGE(time, TD_TIME_ADD(TD_SCHEDULED_TIME(), '-42w'),TD_SCHEDULED_TIME())
group by A.${activity_table_join_key} ,TD_TIME_FORMAT(time,'YYYYMM')
),
T2 AS 
(
select  ${activity_table_join_key},
        yearmonth,
        cnt,
        CAST(FLOOR(avg(cnt)over(PARTITION by ${activity_table_join_key} )) as INTEGER) as avg_cnt,
        row_number()over(partition by ${user_master_join_key} order by yearmonth desc) as rnum 
        from T1
),
T3 AS 
(
SELECT ${activity_table_join_key} ,(CASE WHEN T2.cnt <= T2.avg_cnt then 00
             WHEN T2.cnt > T2.avg_cnt then 01
             else NULL
             end)
         as avg_visit_boolean
FROM T2 where rnum = 1
)
select A.*,coalesce(T3.avg_visit_boolean,100) as td_avg_visit_monthly_trend
from ${enriched_user_master_table_temp} A left outer join T3 
on A.${user_master_join_key} = T3.${activity_table_join_key}