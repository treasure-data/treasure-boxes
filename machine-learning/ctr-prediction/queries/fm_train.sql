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
  avg(Wi) as Wi,
  array_avg(Vif) as Vif
from (
  select
    train_fm(
      features, label,
      "-c -factor ${factor} -iters ${iters} -lambda_w0 ${lambda_w0} -lambda_wi ${lambda_wi} -lambda_v ${lambda_v} -eta ${eta}"
    ) as (feature, Wi, Vif)
  from
    train_oversampling
) t
group by feature;
