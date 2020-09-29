---Code below creates a table of granular channel-source stats, so we can understand the percentage of different ad sources that are part of each marketing channel
WITH T1 as (
select ${channel_col}, ${source_col}, count(${source_col}) as cnt_distinct_source_per_channel
from ${union_table}
group by 1, 2
order by 1, 3 desc
),
T2 as (
select ${channel_col}, count(*) as total_cnt_per_channel
from ${union_table}
group by 1
)
select T1.${channel_col}, T2.total_cnt_per_channel, T1.${source_col}, T1.cnt_distinct_source_per_channel
FROM T1 join T2
on T1.${channel_col} = T2.${channel_col}