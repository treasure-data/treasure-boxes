select
  rmse(p.predicted_cltv, t.cltv) as rmse,
  mae(p.predicted_cltv, t.cltv) as mae
from
  predictions p
join
  cltv_test t
  on p.customerid = t.customerid
