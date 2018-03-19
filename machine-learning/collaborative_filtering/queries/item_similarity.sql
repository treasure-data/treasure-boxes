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
    dimsum_mapper(f.feature_vector, m.mags, '-threshold ${dimsum_similarity_threshold} -disable_symmetric_output')
      as (itemid, other, score)
  from
    item_features f
    left outer join item_magnitude m
),
similarity_upper_triangular as (
  -- if similarity of (i1, i2) pair is in this table, (i2, i1)'s similarity is omitted
  select
    itemid, 
    other,
    sum(score) as similarity
  from 
    partial_result
  group by
    itemid, other
),
similarity as ( -- copy (i1, i2)'s similarity as (i2, i1)'s one
  select itemid, other, similarity from similarity_upper_triangular
  union all
  select other as itemid, itemid as other, similarity from similarity_upper_triangular
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
