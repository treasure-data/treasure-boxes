select
  mae(predicted, actual) as mae,
  rmse(predicted, actual) as rmse
from prediction;
