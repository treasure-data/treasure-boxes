with fm_train_samples as (
  select
    t1.rowid,
    concat_array(t1.features, t2.features) as features,
    t2.label
  from
    train_quantitative t1
    left outer join train_categorical t2 on (t2.rowid = t1.rowid)
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
      "-c -factor ${factor} -iters ${iters} -lambda_w0 ${lambda_w0} -lambda_wi ${lambda_wi} -lambda_v ${lambda_v} -eta ${eta} -int_feature"
    ) as (feature, Wi, Vif)
  from
    fm_train_samples
) t
group by feature;
