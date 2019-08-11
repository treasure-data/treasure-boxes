select
(case when t >= 0 and t <= 5 then 'overnight'
    when t >= 6 and t <= 11 then 'morning'
    when t>= 12 and t<= 17 then 'afternoon'
    when t>= 18 and t <= 23 then 'evening'
    end ) as activity_period, B.*
    from
    (
select
cast(SUBSTR(TD_TIME_FORMAT(${td.timestamp_column},'HH:mm'),1,2) as INTEGER) as t ,A.*
from ${td.original_pageviews} A
) B
