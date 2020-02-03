select
table_schema || '.' || table_name as table_name
,column_name 
,data_type 
,is_nullable
from information_schema.columns
where table_schema='${source_database}' 
and table_name='${source_table}' 


