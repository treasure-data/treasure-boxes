-- Data Cleaning

insert OVERWRITE table temp_table select LOWER(REGEXP_REPLACE(last_first_name,"[^a-zA-Z]","")) as last_first_name,
RANK() OVER (ORDER BY last_first_name asc) as seq_nbr
from fuzzy_data