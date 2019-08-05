-- insert updated record where ${td.param_table} operation is 'update'
-- where foregin key matches with Master table 
-- GDPR field name (ex:email ) of master (as master is  updated  first by wf ) 
--matches with ${td.param_table} table updated value (col :new_value)
INSERT INTO  ${td.each.foreign_db}.${td.each.foreign_table}
SELECT 
  ${td.last_results.column_names},
  B.${td.each.master_fn_name} as ${td.each.master_fn_name},
  TD_TIME_PARSE(CAST (now() as varchar)) as time
from ${td.each.foreign_db}.${td.each.foreign_table} A 
join 
${td.each.master_db}.${td.each.master_table} B
on A.${td.each.foreign_key} = B.${td.each.foreign_key}
join ${td.param_table} C
on B.${td.each.master_fn_name} = C.new_value
WHERE UPPER(C.OPERATION) = 'UPDATE'

