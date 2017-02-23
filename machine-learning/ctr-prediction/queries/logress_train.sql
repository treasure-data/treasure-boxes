with train_oversampling as (
  -- negative samples
  select features, label
  from train
  where label = 0
  union all
  -- over-sampled positive samples
  select features, label
  from (
    select amplify(${pos_oversampling}, features, label) as (features, label)
    from train
    where label = 1
  ) t0
)
-- DIGDAG_INSERT_LINE
select
  feature,
  avg(weight) as weight
from (
  select
    logress(features, label) as (feature, weight)
  from
    train_oversampling
) t
group by feature;
