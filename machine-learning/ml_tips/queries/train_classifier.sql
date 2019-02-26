select
  train_classifier(
    features
    , survived
  ) as (feature, weight)
from
  ${source}
;
