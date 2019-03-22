with amplified as (
  select
    amplify(${oversample_n_times}, features, survived) as (features, survived)
  from
    ${source}
),
train_oversampled as (
  select
    features
    , survived
  from
    amplified
  CLUSTER BY rand(43)
),
model_oversampled as (
  select
    train_classifier(
      features
      , survived
    ) as (feature, weight)
  from
    train_oversampled
)
-- DIGDAG_INSERT_LINE
select
  feature
  , avg(weight) as weight
from
  model_oversampled
group by
  feature
;
