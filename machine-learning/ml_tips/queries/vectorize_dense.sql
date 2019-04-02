-- client: molehill/0.0.1
select
  rowid
  , array(age, fare, mhash(embarked, ${feature_cardinality}), mhash(sex, ${feature_cardinality}), mhash(pclass, ${feature_cardinality})) as features
  , survived
from
  ${source}
;
