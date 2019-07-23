with features_exploded as (
  select
    h.rowid
    ,extract_feature(t.fv) as feature
    ,extract_weight(t.fv) as value
  from
    test h
    LATERAL VIEW explode(add_bias(features)) t as fv
),
prediction as (
  select
    t1.price as actual_price,
    t2.predicted_price
  from
    test t1
  join (
    select
      t1.rowid
      ,sum(m.weight * t1.value) as predicted_price
    from
      features_exploded t1
      LEFT OUTER JOIN regressor${suffix} m ON (t1.feature = m.feature)
    group by
      t1.rowid
  ) t2
  on t1.rowid = t2.rowid
)
-- DIGDAG_INSERT_LINE
select
  rmse(predicted_price, actual_price) as rmse
  ,mae(predicted_price, actual_price) as mae
  , cast(${eta0} as double) as eta0
  , "${reg}" as reg
from
  prediction p
;
