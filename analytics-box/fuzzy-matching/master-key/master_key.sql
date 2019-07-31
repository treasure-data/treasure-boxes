--Master key 

with  temp as(
select last_first_name , group_key from (
    select *, 
    ROW_NUMBER() over (partition by group_key order by group_key desc) rn
    from fuzzy_data
) t1 where rn = 1
)

insert OVERWRITE table temp_table select fuzzy_data.last_first_name,fuzzy_data.group_key,temp.last_first_name as master_key , fuzzy_data.seq_nbr as seq_nbr
from temp , fuzzy_data 
where temp.group_key = fuzzy_data.group_key