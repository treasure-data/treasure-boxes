select
  rand(31) as rnd,
  customerid,
  cltv,
  country,
  recency,
  avg_basket_value,
  avg_basket_size,
  cnt_returns,
  has_returned
from
  cltv
cluster by
  rand(43)
