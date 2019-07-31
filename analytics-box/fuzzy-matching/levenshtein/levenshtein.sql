--Levenshtein

with temp as (
select last_first_name,master_key,group_key,((length(last_first_name) + length(master_key)) - LEVENSHTEIN(last_first_name,master_key))/(length(last_first_name) + length(master_key))*100 as levenshtein_ratio , seq_nbr
from fuzzy_data
)

insert OVERWRITE table temp_table select * from temp