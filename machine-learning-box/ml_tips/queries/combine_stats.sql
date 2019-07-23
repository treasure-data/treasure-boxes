-- client: molehill/0.0.1
select
  train.age_mean as age_mean_train
  , train.age_std as age_std_train
  , train.age_min as age_min_train
  , train.age_25 as age_25_train
  , train.age_median as age_median_train
  , train.age_75 as age_75_train
  , train.age_max as age_max_train
  , test.age_mean as age_mean_test
  , test.age_std as age_std_test
  , test.age_min as age_min_test
  , test.age_25 as age_25_test
  , test.age_median as age_median_test
  , test.age_75 as age_75_test
  , test.age_max as age_max_test
  , whole.age_mean as age_mean
  , whole.age_std as age_std
  , whole.age_min as age_min
  , whole.age_25 as age_25
  , whole.age_median as age_median
  , whole.age_75 as age_75
  , whole.age_max as age_max
  , train.fare_mean as fare_mean_train
  , train.fare_std as fare_std_train
  , train.fare_min as fare_min_train
  , train.fare_25 as fare_25_train
  , train.fare_median as fare_median_train
  , train.fare_75 as fare_75_train
  , train.fare_max as fare_max_train
  , test.fare_mean as fare_mean_test
  , test.fare_std as fare_std_test
  , test.fare_min as fare_min_test
  , test.fare_25 as fare_25_test
  , test.fare_median as fare_median_test
  , test.fare_75 as fare_75_test
  , test.fare_max as fare_max_test
  , whole.fare_mean as fare_mean
  , whole.fare_std as fare_std
  , whole.fare_min as fare_min
  , whole.fare_25 as fare_25
  , whole.fare_median as fare_median
  , whole.fare_75 as fare_75
  , whole.fare_max as fare_max
from
  ${source}_train_stats as train, ${source}_test_stats as test, ${source}_stats as whole
;
