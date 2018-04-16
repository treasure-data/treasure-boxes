select 
  userid,
  itemid,
  max(tstamp) as tstamp,
  count(1) as count
from
  transaction
group by
  userid, itemid
