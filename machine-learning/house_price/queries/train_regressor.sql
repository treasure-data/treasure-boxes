select
  train_regressor(
    add_bias(features)
    ,price
    ,'--loss_function squaredloss --optimizer adagrad -eta0 ${eta0} -iter ${iter}'
  )
from
  training
;
