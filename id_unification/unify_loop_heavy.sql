with hs as (
  select
    key,
    follower,
    cast(conv(substr(sha1(key),1,2),16,10) as bigint) % 4 as h
  from (
    -- emit smallest -> other
    select
      features[0] as key,
      feature as follower
    from ${td.source_tbl}_unify_loop_${i}
    lateral view explode(features) ex as feature
 
    union all
 
    -- emit other -> smallest
    select
      feature as key,
      features[0] as follower
    from ${td.source_tbl}_unify_loop_${i}
    lateral view explode(features) ex as feature
  ) us
)
insert overwrite table ${td.source_tbl}_unify_loop_${i+1}
select
  features
from (
  -- take set of features followed by the key as the new set of features.
  -- 1-element rows were keys which did not connect.
  -- Take first 10 elements only and give up following elements.
  -- This likely removes td_global_id because they have "f:" as prefix which
  -- will come at the end. Number of unique td_global_id may become
  -- large if browser is Mobile Safari.
  select key, array_slice(sort_array(collect_set(follower)), 0, 10) as features
  from hs where h = 0 group by key having size(collect_set(follower)) > 1
  union all
  select key, array_slice(sort_array(collect_set(follower)), 0, 10) as features
  from hs where h = 1 group by key having size(collect_set(follower)) > 1
  union all
  select key, array_slice(sort_array(collect_set(follower)), 0, 10) as features
  from hs where h = 2 group by key having size(collect_set(follower)) > 1
  union all
  select key, array_slice(sort_array(collect_set(follower)), 0, 10) as features
  from hs where h = 3 group by key having size(collect_set(follower)) > 1
) ds