select
  logloss(t1.predicted_ctr, t2.label) as logloss
from
  prediction t1
  inner join test t2 on (t1.rowid = t2.rowid)
;
