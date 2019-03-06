select
  auc(${predicted_column}, survived) as auc
  , logloss(${predicted_column}, survived) as logloss
from
  (
    select
      p.${predicted_column}, t.survived
    from
      ${predicted_table} p
    join
      ${actual} t on (p.rowid = t.rowid)
    order by
      probability desc
  ) t2
;
