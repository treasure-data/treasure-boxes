select
  avg(pclass) as pclass_mean
  , stddev_pop(pclass) as pclass_std
  , min(pclass) as pclass_min
  , approx_percentile(pclass, 0.25) as pclass_25
  , approx_percentile(pclass, 0.5) as pclass_median
  , approx_percentile(pclass, 0.75) as pclass_75
  , max(pclass) as pclass_max
  , avg(age) as age_mean
  , stddev_pop(age) as age_std
  , min(age) as age_min
  , approx_percentile(age, 0.25) as age_25
  , approx_percentile(age, 0.5) as age_median
  , approx_percentile(age, 0.75) as age_75
  , max(age) as age_max
  , avg(sibsp) as sibsp_mean
  , stddev_pop(sibsp) as sibsp_std
  , min(sibsp) as sibsp_min
  , approx_percentile(sibsp, 0.25) as sibsp_25
  , approx_percentile(sibsp, 0.5) as sibsp_median
  , approx_percentile(sibsp, 0.75) as sibsp_75
  , max(sibsp) as sibsp_max
  , avg(parch) as parch_mean
  , stddev_pop(parch) as parch_std
  , min(parch) as parch_min
  , approx_percentile(parch, 0.25) as parch_25
  , approx_percentile(parch, 0.5) as parch_median
  , approx_percentile(parch, 0.75) as parch_75
  , max(parch) as parch_max
  , avg(fare) as fare_mean
  , stddev_pop(fare) as fare_std
  , min(fare) as fare_min
  , approx_percentile(fare, 0.25) as fare_25
  , approx_percentile(fare, 0.5) as fare_median
  , approx_percentile(fare, 0.75) as fare_75
  , max(fare) as fare_max
  , avg(body) as body_mean
  , stddev_pop(body) as body_std
  , min(body) as body_min
  , approx_percentile(body, 0.25) as body_25
  , approx_percentile(body, 0.5) as body_median
  , approx_percentile(body, 0.75) as body_75
  , max(body) as body_max
from
  ${source}
;
