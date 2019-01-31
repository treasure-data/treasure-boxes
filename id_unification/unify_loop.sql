insert overwrite table ${td.source_tbl}_unify_loop_${i+1}
select
  -- Take first 10 elements only and give up following elements.
  -- This likely removes td_global_id because they have "f:" as prefix which
  -- will come at the end. Number of unique td_global_id may become
  -- large if browser is Mobile Safari.
  array_slice(sort_array(followers), 0, 10) as features
from (
  -- take set of features followed by the key as the new set of features
  select
    key,
    collect_set(follower) as followers
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
  group by key
) es
-- 1-element rows were keys which did not connect
where size(followers) > 1
;
