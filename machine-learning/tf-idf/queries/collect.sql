select
  docid,
  collect_list(feature(word, tfidf)) as tfidf
from
  tfidf
group by
  docid
