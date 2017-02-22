with logress_test_samples as (
  select
    t1.rowid,
    concat_array(t1.features, t2.features) as features
  from
    test_quantitative t1
    left outer join test_categorical t2 on (t2.rowid = t1.rowid)
),
logress_test_exploded as (
  select
    rowid,
    extract_feature(fv) as feature,
    extract_weight(fv) as value
  from
    logress_test_samples t1 LATERAL VIEW explode(features) t2 as fv
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
