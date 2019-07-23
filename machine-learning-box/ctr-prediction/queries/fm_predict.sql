with fm_test_exploded as (
  select
    rowid,
    extract_feature(fv) as feature,
    extract_weight(fv) as Xi
  from
    test t1 LATERAL VIEW explode(features) t2 as fv
),
score as (
  select
    t1.rowid,
    -- original predicted CTR
    sigmoid( fm_predict(p1.Wi, p1.Vif, t1.Xi) ) as p
  from
    fm_test_exploded t1
    LEFT OUTER JOIN fm_model p1 ON (t1.feature = p1.feature)
  group by
    t1.rowid
)
-- DIGDAG_INSERT_LINE
select
  t.rowid,
  -- use calibrated CTR to prevent negative effect of over-sampling
  t.p / (t.p + (1.0 - t.p) / ${td.last_results.downsampling_rate}) AS predicted_ctr
from
  score t
;
