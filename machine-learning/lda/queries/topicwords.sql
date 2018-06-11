select 
  label as topic,
  to_ordered_list(word, rnk) as words 
from
  ranked_words
group by
  label
order by
  label asc
;