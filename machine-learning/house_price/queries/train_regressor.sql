select
  train_regressor(
    features
    ,price
    ,'--loss_function squaredloss --optimizer adagrad'
  )
from
  training