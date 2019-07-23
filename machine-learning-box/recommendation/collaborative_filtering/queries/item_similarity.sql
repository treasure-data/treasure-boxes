-- @TD distribute_strategy: aggressive
with item_magnitude as ( -- compute magnitude of each item vector
  select
    to_map(j, mag) as mags
  from (
    select 
      itemid as j,
      l2_norm(ln(count+1)) as mag -- use scaled value
    from 
      user_item
    group by
      itemid
  ) t0
),
item_features as (
  select
    userid as i,
    collect_list(
      feature(itemid, round(ln(count+1),5)) -- use scaled value
    ) as feature_vector
  from
    user_item
  group by
    userid
),
partial_result as (
  select
    dimsum_mapper(f.feature_vector, m.mags, '-threshold ${dimsum_similarity_threshold}')
      as (itemid, other, score)
  from
    item_features f
    left outer join item_magnitude m
),
similarity as (
  select
    itemid, 
    other,
    sum(score) as similarity
  from 
    partial_result
  group by
    itemid, other
),
topk as (
  select
    each_top_k( -- get top-10 items based on similarity score
      ${topk_similar_items}, itemid, similarity,
      itemid, other -- output items
    ) as (rank, similarity, itemid, other)
  from (
    select * from similarity
    CLUSTER BY itemid
  ) t
)
-- DIGDAG_INSERT_LINE
select 
  itemid, other, similarity
from 
  topk
