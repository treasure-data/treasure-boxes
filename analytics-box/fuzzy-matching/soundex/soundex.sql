--Soundex algortihm

insert OVERWRITE table temp_table
select last_first_name,SOUNDEX(last_first_name) as group_key , seq_nbr
from fuzzy_data