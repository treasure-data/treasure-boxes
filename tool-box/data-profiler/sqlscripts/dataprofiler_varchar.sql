select
 '${source_database}' as  db 
 ,'${source_table}' as tbl 
 ,'${column}' as  column
 ,(select COUNT_IF(${column} is NULL) from ${source_database}.${source_table}) as null_cnt
,(select approx_distinct(${column}) from ${source_database}.${source_table}) as aprx_distinct_cnt 
,(select MIN(LENGTH(${column})) from  ${source_database}.${source_table}) as min_length
,(select MIN(LENGTH(${column}),${min_max_limit}) from  ${source_database}.${source_table}) as min_${min_max_limit}_val
,(select MAX(LENGTH(${column}),${min_max_limit}) from  ${source_database}.${source_table}) as max_${min_max_limit}_val
 from ${source_database}.${source_table} limit 1
