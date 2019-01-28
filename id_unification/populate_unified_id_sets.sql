insert overwrite table ${td.source_tbl}_unified_id_sets
select
  feature as join_id,
  features[0] as canonical_id
from ${td.source_tbl}_unify_loop_6  -- change this number to point results of the last loop
lateral view explode(features) ex as feature