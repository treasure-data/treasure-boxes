select
  logloss(predicted_ctr, 1.0) as logloss
from
  prediction
;
