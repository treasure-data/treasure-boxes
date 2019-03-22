select
  rowid
  , survived
  , zscore(
    age
    , ${td.last_results.age_mean}
    , ${td.last_results.age_std}
  ) as age
  , zscore(
    fare
    , ${td.last_results.fare_mean}
    , ${td.last_results.fare_std}
  ) as fare
  , embarked
  , sex
  , pclass
from
  ${source}
;
