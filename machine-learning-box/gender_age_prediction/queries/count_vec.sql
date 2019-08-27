WITH document_frequency AS (
  select
    word,
    count(distinct userid) docs
  from
    exploded
  group by
    word
  having   
    count(distinct userid) >= 2
),
wordcnt as (
  select
    l.userid,
    l.word,
    ln(1+count(1)) as cnt -- logscale count
  from
    exploded l
    LEFT SEMI JOIN document_frequency r ON (l.word = r.word)
  group by
    l.userid,
    l.word
),
rescaled as (
  select
    userid, 
    word, 
    rescale(cnt, min(cnt) over (partition by word), max(cnt) over (partition by word)) as value
  from
    wordcnt
)
-- DIGDAG_INSERT_LINE
select
  userid,
  to_ordered_list(feature(word,value), value, '-k ${num_features}') as features
from
  rescaled
group by
  userid
