-- Data Cleaning

insert OVERWRITE table temp_table select LOWER(REGEXP_REPLACE(${td.column},"[^a-zA-Z]","")) as last_first_name,
RANK() OVER (ORDER BY ${td.column} asc) as seq_nbr
from ${td.table}
