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
    train
) t
group by feature;
