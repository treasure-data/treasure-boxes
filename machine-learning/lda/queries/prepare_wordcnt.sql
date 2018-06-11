WITH word_counts as (
  select
    docid,
    word,
	count(1) as cnt
  from 
    tokenized
  group by
    docid, word
)
-- DIGDAG_INSERT_LINE
select 
  docid,
  collect_list(feature(translate(word,':','\;'),cnt)) as features
from 
  word_counts
where
  cnt >= 2
group by 
  docid
CLUSTER by rand(43) -- random shuffling
;