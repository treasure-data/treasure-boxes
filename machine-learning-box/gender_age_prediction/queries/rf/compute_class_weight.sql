-- DIGDAG_INSERT_LINE
WITH tmp1 as (
  select 
    label,
    gender_age,
    cast(count(1) as double) as cnt
  from
    rf_input
  group by 
    1, 2
),
tmp2 as (
  select
    label,
    gender_age,
    cnt,
    cnt / sum(cnt) over () * 100.0 as cnt_perc,
    ln(1.0 / (cnt / sum(cnt) over () * 100.0) + 1.0) as x -- inverse scaling over l1 norm レコード数の逆数のログ
  from
    tmp1
),
tmp3 as (
  select
    label,
    gender_age,
    cnt,
    cnt_perc,
    x,
    min(x) over () as x_min,
    max(x) over () as x_max
  from
    tmp2
)
select
  label,
  gender_age,
  cnt,
  cnt_perc,
  x,
  ((x - x_min) / (x_max - x_min)) * (${max_class_weight} - ${min_class_weight}) + ${min_class_weight} as class_weight -- min-max scaling
from 
  tmp3