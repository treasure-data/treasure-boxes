-- Hive
select
  rowid() as id
  , pclass, survived, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked, boat, body, home_dest
  -- stratified sampling
  count(1) over (partition by label) as per_label_count,
  -- Presto doesn't have a way to pass random seed. This SQL isn't reproducibile.
  rank() over (partition by label order by rand(41)) as rank_in_label
from
  ${source}
;