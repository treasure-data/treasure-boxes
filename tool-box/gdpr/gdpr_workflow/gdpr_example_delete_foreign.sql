DELETE FROM ${td.each.foreign_db}.${td.each.foreign_table}
 WHERE ${td.each.foreign_key} IN (
	SELECT ${td.each.foreign_key} 
	FROM ${td.each.master_db}.${td.each.master_table} WHERE ${td.each.master_fn_name} 
	IN ( SELECT ${td.each.master_fn_name} FROM ${td.param_table} 
	WHERE operation = 'DELETE' )
)