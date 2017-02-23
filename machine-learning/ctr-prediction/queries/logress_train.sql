select
  feature,
  avg(weight) as weight
from (
  select
    logress(features, label) as (feature, weight)
  from
    train
) t
group by feature;
