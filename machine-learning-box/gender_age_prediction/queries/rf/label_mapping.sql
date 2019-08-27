-- DIGDAG_INSERT_LINE
select
  gender_age as label,
  rank - 1 as label_id
from (
  select
    distinct gender_age,
    dense_rank() over (order by gender_age asc) as rank
  from 
    input
  where
    gender_age is not null
) t
