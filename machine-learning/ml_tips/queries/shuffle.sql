-- client: molehill/0.0.1
select
  rowid() as rowid
  , survived
  , age
  , fare
  , embarked
  , sex
  , pclass
  , rand(32) as rnd
from
  ${source}
cluster by rand(43)
;
