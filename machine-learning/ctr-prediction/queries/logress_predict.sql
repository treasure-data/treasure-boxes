with logress_test_exploded as (
  select
    rowid,
    extract_feature(fv) as feature,
    extract_weight(fv) as value
  from
    test t1 LATERAL VIEW explode(features) t2 as fv
)
-- DIGDAG_INSERT_LINE
select
  t1.rowid,
  sigmoid( sum(p1.weight * t1.value) ) as predicted_ctr
from
  logress_test_exploded t1
  LEFT OUTER JOIN logress_model p1 ON (t1.feature = p1.feature)
group by
  t1.rowid
;
