select
  '${source_database}' as  db 
  ,'$(source_table}' as tbl 
 ,'${column}' as  ${column} 
 ,(select count(${column}) from ${source_database}.${source_table}) as total_count
,(select approx_distinct(${column}) from ${source_database}.${source_table}) as distinct_val 
,(select avg(${column}) from ${source_database}.${source_table} ) as avg_value
,(select MAX(${column},5) from ${source_database}.${source_table}) as max_five_val
,(select MIN(${column},5) from ${source_database}.${source_table}) as min_five_val
,(select MIN(${column}) from  ${source_database}.${source_table}) as total_MIN
,(select MAX(${column}) from  ${source_database}.${source_table}) as total_MAX
 from ${source_database}.${source_table} limit 1