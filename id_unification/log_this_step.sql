insert into ${td.source_tbl}_loop_steps
select 
  '${table_name}' tbl_name, 
  cast(now() as varchar) completed_at,
  count(1) rows 
from 
  ${table_name};