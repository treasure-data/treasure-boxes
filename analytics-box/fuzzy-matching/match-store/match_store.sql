--Match Store


insert OVERWRITE table match_store select group_key as group_key, collect_list(seq_nbr) as groups
FROM fuzzy_data
GROUP BY group_key
