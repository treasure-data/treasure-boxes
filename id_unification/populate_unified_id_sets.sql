insert overwrite table ${td.source_tbl}_unified_id_sets
select
  feature as join_id,
  features[0] as canonical_id
from 
  ${td.source_tbl}_unify_loop_${td.loops}  
lateral view explode(features) ex as feature