-- client: molehill/0.0.1
with p as (
  select
    model_id
    , model_weight
    , model
  from
    ${model_table}
  DISTRIBUTE BY rand(1)
),
t1 as (
  select
    t.rowid
    , p.model_weight
    , tree_predict(p.model_id, p.model, t.features, "-classification") as predicted
  from
    p
  left outer join ${target_table} t
),
ensembled as (
  select
    rowid
    , rf_ensemble(predicted.value, predicted.posteriori, model_weight) as predicted
  from
    t1
  group by
    rowid
)
-- DIGDAG_INSERT_LINE
select
  rowid
  , predicted.label
  , predicted.probabilities[1] as probability
from
  ensembled
;
