 with valfreqtbl as 
 (select 
  '${source_database}.${source_table}' as schema 
 ,'${column}' as col_name
  ,${column} as col_value 
,count(${column}) as frequency 
from ${source_database}.${source_table}
group by 1,2,3  
order by 1,2,3 desc 
limit 5 )
select * from  valfreqtbl