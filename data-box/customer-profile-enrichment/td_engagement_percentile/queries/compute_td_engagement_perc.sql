WITH T1 AS 
(
SELECT
A.*,
TD_SESSIONIZE_WINDOW(time,${session_windows_time}) 
 OVER (
PARTITION BY ${session_key} , ${session_key_ip}
ORDER BY time)
 as session_id
 FROM
 ${activity_table} A
 ),
T2 AS 
(
select 
session_id,
${session_key},
count(*) as cnt 
from T1
group by session_id,${session_key}
),
T3 AS 
(
select count(*)over (partition by ${session_key}) as rnk,
sum(cnt)over(partition by ${session_key}) as sume,
A.*
FROM T2 A
) ,
T4 AS 
(
select 
${session_key},
CAST(max(rnk) as double) rnke,
CAST(max(sume) as double) as sume,
CAST(max(sume)/max(rnk) as double ) as avg_visit
from T3 
group by ${session_key}
),
T5 AS
(
select row_number()over(order by avg_visit desc ) as rnum,
${session_key}
FROM T4
),
T6 AS 
(
select CAST((SELECT max(rnum) FROM T5) as double) tot_user,
CAST(rnum as double) as actual_rank,
${session_key}
FROM T5
),
T7 AS
(
SELECT CAST(FLOOR((1 - actual_rank / tot_user) * 100) as INTEGER) as td_engagement_perc,
${session_key}
from T6
)
SELECT  T.*, (case when td_engagement_perc >= 1 and td_engagement_perc <= 20 then   1 
                    when  td_engagement_perc >= 21 and td_engagement_perc <= 40 then  2
                    when  td_engagement_perc >= 41 and td_engagement_perc <= 60 then  3
                    when  td_engagement_perc >= 61 and td_engagement_perc <= 80 then  4
                    when  td_engagement_perc >= 81 and td_engagement_perc <= 100 then 5
                    when  td_engagement_perc is null then 0
                    end ) as td_engagement_percentile  From 
${enriched_user_master_table_temp} T left outer join T7 
on T.${user_master_join_key} = T7.${activity_table_join_key}



