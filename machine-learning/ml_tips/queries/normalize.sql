select
  rowid
  , survived
  , zscore(
    age
    , ${td.last_results.age_mean_train}
    , ${td.last_results.age_std_train}
  ) as age
  , zscore(
    fare
    , ${td.last_results.fare_mean_train}
    , ${td.last_results.fare_std_train}
  ) as fare
  , embarked
  , sex
  , pclass
from
  ${source}
;
