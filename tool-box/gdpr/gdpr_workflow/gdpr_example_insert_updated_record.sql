-- insert updated record in master where ${td.param_table} operation is 'update'
-- where value of fieldname matches with ${td.param_table} table old value of fieldname
--update with new value present in ${td.param_table}  table
INSERT INTO  ${td.each.database}.${td.each.table}
SELECT 
  ${td.last_results.column_names},
  B.new_value as ${td.each.fieldname},
  TD_TIME_PARSE(CAST (now() as varchar)) as time
from ${td.each.database}.${td.each.table} A join ${td.param_table} B
on A.${td.each.fieldname} = B.${td.each.fieldname}
WHERE UPPER(B.OPERATION) = 'UPDATE'