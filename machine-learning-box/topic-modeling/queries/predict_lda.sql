-- @TD reducers: 10
WITH exploded as (
  select
    l.docid, 
    extract_feature(feature) as word, 
    extract_weight(feature) as value
  from
    input l
    LATERAL VIEW explode(features) r as feature
),
predicted as (
  select
    t.docid,
    lda_predict(t.word, t.value, m.label, m.lambda, '-topics ${num_topics}') as probabilities
  from
    exploded t
    JOIN lda_model m ON (t.word = m.word)
  group by
    t.docid
)
-- DIGDAG_INSERT_LINE
select 
  docid, 
  probabilities[0].label as topic1, probabilities[0].probability as proba1,
  probabilities[1].label as topic2, probabilities[1].probability as proba2
from
  predicted
;
