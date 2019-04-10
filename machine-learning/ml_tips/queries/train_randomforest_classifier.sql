-- client: molehill/0.0.1
select
  train_randomforest_classifier(
    features
    , survived
    , '-trees 15 -seed 31 -attrs Q,Q,C,C,C'
  )
from
  ${source}
;
