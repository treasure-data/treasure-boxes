WITH T1 AS 
(
select A.${activity_table_join_key},sum((case 
                          when ${utm_source_column} like '%?utm_medium%' then 1 
                          when ${utm_source_column} like '%?utm_campaign%' then 1    
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
  CAST(FLOOR((1 - utm_rank / total_user) * 100) as INTEGER) as td_ad_exposure_percentile
  FROM T3
)
SELECT u.*,(case when  td_ad_exposure_percentile >= 1 and td_ad_exposure_percentile <= 20 then   1 
                    when  td_ad_exposure_percentile >= 21 and td_ad_exposure_percentile <= 40 then  2
                    when  td_ad_exposure_percentile >= 41 and td_ad_exposure_percentile <= 60 then  3
                    when  td_ad_exposure_percentile >= 61 and td_ad_exposure_percentile <= 80 then  4
                    when  td_ad_exposure_percentile >= 81 and td_ad_exposure_percentile <= 100 then 5
                    when  td_ad_exposure_percentile is null then 0
                    end ) as td_ad_exposure_percentile
from ${enriched_user_master_table_temp} u left outer join T4
on u.${user_master_join_key} = T4.${activity_table_join_key}

