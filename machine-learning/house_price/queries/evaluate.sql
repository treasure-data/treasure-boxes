select
  rmse(p.predicted_price, t.price) as rmse
  ,mae(p.predicted_price, t.price) as mae
from
  predictions${suffix} p
join
  test t on (p.rowid = t.rowid)
;
