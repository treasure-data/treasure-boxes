select 
  min(depth) as min_depth, max(depth) as max_depth,
  min(position) as min_pos, max(position) as max_pos
from
  ${in_db}.training
;