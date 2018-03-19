WITH topk as (
  select
    each_top_k(
       ${max_recommended_items}, userid, similarity,
       userid, other
    ) as (rank, similarity, userid, rec_item)
  from (
    select
      t1.userid, t2.other, max(t2.similarity) as similarity
    from
      recent_item_contacts t1
      JOIN item_similarity t2 ON (t1.itemid = t2.itemid)
    where
      t1.itemid != t2.other -- do not include items that user already purchased
      AND NOT EXISTS (
        SELECT a.itemid FROM user_item a
        WHERE a.userid = t1.userid AND a.itemid = t2.other
--        AND a.count <= 1 -- optional filtering
      )
    group by
      t1.userid, t2.other
    CLUSTER BY
      userid -- top-k grouping by userid
  ) t1
)
-- DIGDAG_INSERT_LINE
select
  userid,
  to_ordered_list(rec_item, rank) as rec_items
from
  topk
group by
  userid
;