select
  u1.itemid,
  u2.itemid as other, 
  count(1) as cnt
from
  user_item u1
  JOIN user_item u2 ON (u1.userid = u2.userid)
where
  u1.itemid != u2.itemid 
group by
  u1.itemid, u2.itemid