-- client: molehill/0.0.1
select
  rowid
  , array(
    age, fare
    -- `feature_cardinality` is a workaround to avoid this issue: https://issues.apache.org/jira/projects/HIVEMALL/issues/HIVEMALL-243
    , mhash(embarked, ${feature_cardinality}), mhash(sex, ${feature_cardinality}), mhash(pclass, ${feature_cardinality})
  ) as features
  , survived
from
  ${source}
;
