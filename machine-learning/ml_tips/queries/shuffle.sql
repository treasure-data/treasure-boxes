-- Hive
select
  rowid() as id
  , rand(31) as rnd
  , pclass, survived, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked, boat, body, home_dest
from
  ${source}
cluster by rand(43)
;
