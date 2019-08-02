DELETE FROM ${td.each.database}.${td.each.table} 
WHERE ${td.each.fieldname} IN
 (SELECT ${td.each.fieldname} from ${td.param_table} WHERE operation = 'DELETE')