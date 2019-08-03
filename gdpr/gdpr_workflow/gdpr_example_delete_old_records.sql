--Delete old records from master which matches the old  value of field name from ${td.param_table} 
Delete from ${td.each.database}.${td.each.table}
where ${td.each.fieldname} in (select ${td.each.fieldname} from ${td.param_table} 
where upper(operation) = 'UPDATE')