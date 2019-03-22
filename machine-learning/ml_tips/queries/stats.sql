select
  avg(age) as age_mean
  , stddev_pop(age) as age_std
  , min(age) as age_min
  , approx_percentile(age, 0.25) as age_25
  , approx_percentile(age, 0.5) as age_median
  , approx_percentile(age, 0.75) as age_75
  , max(age) as age_max
  , avg(fare) as fare_mean
  , stddev_pop(fare) as fare_std
  , min(fare) as fare_min
  , approx_percentile(fare, 0.25) as fare_25
  , approx_percentile(fare, 0.5) as fare_median
  , approx_percentile(fare, 0.75) as fare_75
  , max(fare) as fare_max
from
  ${source}
;
