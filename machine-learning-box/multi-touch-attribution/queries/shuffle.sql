-- Code below assigns ab_rnd attribute to each unique user for the random shuffling of TensorFlow record creation
WITH T1 as (
  select 
    distinct ${unique_id} 
  from 
    ${in_table}
),
T2 as (
  select
    rand(18) as ab_rnd,
    ${unique_id}
  from
    T1
  cluster by
    rand(43)
)
-- DIGDAG_INSERT_LINE
select 
  A.*, 
  T2.ab_rnd 
from 
  ${in_table} A
join T2 
  on A.${unique_id} = T2.${unique_id}