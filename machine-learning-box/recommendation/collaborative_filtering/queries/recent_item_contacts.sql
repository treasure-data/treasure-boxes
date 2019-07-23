select
  each_top_k( -- get recently contacted items for each user
     ${recent_items}, userid, tstamp,
     userid, itemid
  ) as (rank, tstamp, userid, itemid)
from (
  select
    tstamp, userid, itemid
  from 
    user_item
  CLUSTER BY
    userid
) t
