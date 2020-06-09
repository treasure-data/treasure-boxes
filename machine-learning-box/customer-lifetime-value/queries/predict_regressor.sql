with features_exploded as (
  select
    t.customerid,
    extract_feature(t.fv) as feature,
    extract_weight(t.fv) as value
  from
    cltv_test_vectorized t
    LATERAL VIEW explode(add_bias(features)) t as fv
)
-- DIGDAG_INSERT_LINE
select
  t.customerid,
  sum(m.weight * t.value) as predicted_cltv
from
  features_exploded t
  LEFT OUTER JOIN regressor m ON (t.feature = m.feature)
group by
  t.customerid
