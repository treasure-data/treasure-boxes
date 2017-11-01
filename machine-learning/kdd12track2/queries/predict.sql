WITH exploded as (
  select 
    l.rowid,
    extract_feature(t.feature) as feature,
    extract_weight(t.feature) as value
  from
    kddcup_test l
    LATERAL VIEW explode(features) t AS feature
)
-- DIGDAG_INSERT_LINE
select
  t.rowid, 
  sigmoid(sum(m.weight * t.value)) as prob
from 
  exploded t
  LEFT OUTER JOIN kddcup_lr_model m ON (t.feature = m.feature)
group by 
  t.rowid
;