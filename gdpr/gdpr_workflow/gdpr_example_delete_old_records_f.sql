--After insert Delete  old records where 
--foreign key  matches with master table 
-- fieldname(ex:email) of foreign table matches with old ${td.param_table} field name 


DELETE 
FROM
  ${td.each.foreign_db}.${td.each.foreign_table}
WHERE (${td.each.foreign_key}) IN
(
    SELECT 
      A.${td.each.foreign_key}
    FROM
      ${td.each.master_db}.${td.each.master_table} A
    JOIN
      ${td.param_table} B
      ON A.${td.each.master_fn_name} = B.new_value
    WHERE
      UPPER(OPERATION)= 'UPDATE'
  )
  AND ${td.each.master_fn_name} IN
  (
    SELECT 
      B.${td.each.master_fn_name}
    FROM
      ${td.each.master_db}.${td.each.master_table} A
    JOIN
      ${td.param_table} B
      ON A.${td.each.master_fn_name} = B.new_value
    WHERE
      UPPER(OPERATION)= 'UPDATE'
  )
