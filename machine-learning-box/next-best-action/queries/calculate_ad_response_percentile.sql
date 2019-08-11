WITH T1 AS
(
select A.${activity_table_join_key},sum((case
                          when ${utm_source_column} like '%${td.each.ad_response}%' then 1
                          else 0
                          end)) as no_of_visit
from ${activity_table} A
group by ${activity_table_join_key}
) ,
T2 AS
(
select ${activity_table_join_key},
row_number()over(order by no_of_visit desc) as utm_rank
FROM T1
),
T3 AS
(
SELECT
   ${activity_table_join_key},
  CAST((SELECT max(utm_rank) FROM t2) as double) total_user,
  CAST(utm_rank as double) as utm_rank
  FROM T2
),
T4 as (
  SELECT
   ${activity_table_join_key},
  CAST(FLOOR((1 - utm_rank / total_user) * 100) as INTEGER) as td_e
  FROM T3
)
SELECT u.*,coalesce(td_e,0) as ${td.each.var_name}
from ${enriched_user_master_table_temp} u left outer join T4
on u.${user_master_join_key}= T4.${activity_table_join_key}
