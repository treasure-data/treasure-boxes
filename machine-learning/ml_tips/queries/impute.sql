select
  rowid
  , survived
  , coalesce(age, ${td.last_results.age_median_train}) as age
  , coalesce(fare, ${td.last_results.fare_median_train}) as fare
  , coalesce(cast(embarked as varchar), 'missing') as embarked
  , coalesce(cast(sex as varchar), 'missing') as sex
  , coalesce(cast(pclass as varchar), 'missing') as pclass
from
  ${source}
;
