select
  '${source_database}' as db
 , '${source_table}' as  tbl 
 ,'${column}' as  ${column} 
 ,(select count(${column}) from ${source_database}.${source_table}) as total_count
 ,(select count(${column}) from ${source_database}.${source_table} where ${column} is NULL) as total_null_count
, (select  approx_distinct(${column}) from ${source_database}.${source_table}) as distinct_val 
,(select avg(${column}) from ${source_database}.${source_table} ) as avg_value
,(select max(cast(${column} as int),${min_max_limit}) from ${source_database}.${source_table}) as max_${min_max_limit}_val
,(select min(cast(${column} as int),${min_max_limit}) from ${source_database}.${source_table}) as min_${min_max_limit}_val
,(select MIN(${column}) from  ${source_database}.${source_table}) as total_MIN
,(select MAX(${column}) from  ${source_database}.${source_table}) as total_MAX
 from ${source_database}.${source_table} limit 1