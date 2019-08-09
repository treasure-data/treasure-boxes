SELECT 
	column_name,
	is_nullable,
	data_type,
	extra_info 
FROM information_schema.columns
WHERE 
	table_name LIKE '${td.each.staging_table}' 
	AND 
	table_schema LIKE '${td.each.staging_database}'
EXCEPT 
	SELECT 
		column_name,
		is_nullable,
		data_type,
		extra_info 
	FROM information_schema.columns 
	WHERE 
		table_name LIKE '${td.each.final_table}' 
		AND 
		table_schema LIKE '${td.each.final_database}'