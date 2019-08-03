DROP TABLE IF EXISTS tmp_inform_foreign_keys;
CREATE TABLE tmp_inform_foreign_keys AS
SELECT 
${td.each.foreign_key} foreign_key, 
${td.each.master_fn_name} master_key
FROM ${td.each.master_db}.${td.each.master_table} 
WHERE ${td.each.master_table}.${td.each.master_fn_name} IN 
( SELECT ${td.each.master_fn_name} FROM ${td.param_table} WHERE operation = 'INFORM' );