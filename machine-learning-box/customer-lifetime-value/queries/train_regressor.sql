select
  train_regressor(
    add_bias(features),
    cltv
  )
from
  cltv_train_vectorized
