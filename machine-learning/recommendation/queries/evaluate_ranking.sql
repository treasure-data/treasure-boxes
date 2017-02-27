select
  ndcg(t1.recommended_items, t2.truth_items) as ndcg
from
  recommendation t1 join (
    select
      userid,
      collect_set(itemid) as truth_items
    from testing_mf
    where rating >= 4.0 -- threshold for positive events
    group by userid
  ) t2 on (t1.userid = t2.userid)
;
