with features_exploded as (
  select
    rowid
    , extract_feature(fv) as feature
    , extract_weight(fv) as value
  from
    ${target_table} t1
    LATERAL VIEW explode(features) t2 as fv
)
-- DIGDAG_INSERT_LINE
select
  t1.rowid
  , sigmoid(sum(m1.weight * t1.value)) as probability
from
  features_exploded t1
  left outer join ${model_table} m1
    on (t1.feature = m1.feature)
group by
  t1.rowid
;
