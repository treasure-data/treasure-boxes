with actual_cnt as (
  SELECT
    actual as gender_age,
    sum(cnt) as actual_cnt
  FROM 
    rf_confusion_matrix
  group by
    1
),
predicted_cnt as (
  SELECT
    predicted as gender_age,
    sum(cnt) as predicted_cnt
  FROM 
    rf_confusion_matrix
  group by
    1
)
select
  l.gender_age,
  l.actual_cnt,
  r1.predicted_cnt,
  (cast(l.actual_cnt+r1.predicted_cnt as double))/least(cast(l.actual_cnt as double),cast(r1.predicted_cnt as double)) as diff
  ,r2.cnt
  ,r2.cnt_perc
  ,r2.class_weight
  ,r2.cnt * r2.class_weight as sampled
from
  actual_cnt l
  join predicted_cnt r1 on (l.gender_age = r1.gender_age)
  join class_weight r2 on (l.gender_age = r2.gender_age)
order by
  diff desc