select
  userid,
  map_values(to_ordered_map(rank, itemid)) as recommended_items
from
  top_k
group by
  userid
;
