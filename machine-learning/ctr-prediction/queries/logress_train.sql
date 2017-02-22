with logress_train_samples as (
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
  avg(weight) as weight
from (
  select
    logress(features, label) as (feature, weight)
  from
    logress_train_samples
) t
group by feature;
