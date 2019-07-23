select
  itemid, to_ordered_list(other, similarity, '-reverse -k ${max_recommended_items}') as similar_items
from 
  item_similarity
group by
  itemid