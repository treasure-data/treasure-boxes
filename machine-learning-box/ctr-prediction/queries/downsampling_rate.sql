with t1 as (
  select
    label,
    cast(count(1) as double) as cnt
  from
    train
  group by
    label
),
t2 as (
  select
    map_agg(label, cnt) as kv
  from
    t1
)
select
  -- compute downsampling rate
  (kv[0] / (kv[0] + kv[1] * ${pos_oversampling}.0)) / (kv[0] / (kv[0] + kv[1])) as downsampling_rate
from
  t2
