select array_agg(column_name) as column_details
from ${source_table}_column_metadata
where data_type='bigint' 
and column_name not in ('time')