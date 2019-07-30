WITH T1 AS(
SELECT 
    A.${activity_table_join_key},
    ROW_NUMBER() over(PARTITION BY ${activity_table_join_key} ORDER BY  ${td_intent_key} DESC  ) AS rnk,
   A.${td_intent_key}
    FROM ${activity_table} A
    
),
T2 AS
(
select T1.*,ROW_NUMBER()over(order by ${td_intent_key} desc ) as rnke from T1
where rnk = 1
),   
T3 AS 
(
select CAST((SELECT max(rnke) FROM T2) as double) tot_user,
CAST(rnke as double) as actual_rank,
T2.${activity_table_join_key}
FROM T2 
)  ,    
T4 AS
(
Select
CAST(FLOOR((1 - actual_rank / tot_user) * 100) as INTEGER) as td_intent_perc,
${activity_table_join_key}
FROM T3
) 
SELECT  T.*,(case when td_intent_perc >= 1 and td_intent_perc <= 20 then   1 
                    when  td_intent_perc >= 21 and td_intent_perc <= 40 then  2
                    when  td_intent_perc >= 41 and td_intent_perc <= 60 then  3
                    when  td_intent_perc >= 61 and td_intent_perc <= 80 then  4
                    when  td_intent_perc >= 81 and td_intent_perc <= 100 then 5
                    when  td_intent_perc is null then 0
                    end ) as td_intent_percentile
 From                                        
${enriched_user_master_table_temp} T left outer join T4 
on T.${user_master_join_key} = T4.${activity_table_join_key}

