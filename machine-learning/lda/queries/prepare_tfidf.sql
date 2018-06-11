WITH tf AS (
  select
    docid,
    word,
    freq
  from (
    select
      docid,
      tf(word) as word2freq
    from
      tokenized
    group by
      docid
  ) t
  LATERAL VIEW explode(word2freq) t2 as word, freq
),
df AS (
  select
    word,
    count(distinct docid) docs
  from
    tokenized
  group by
    word
),
tfidf AS (
  select
    tf.docid,
    tf.word,
    tfidf(tf.freq, df.docs, ${n_docs}) as tfidf
  from
    tf
    JOIN df ON (tf.word = df.word)
  where
    df.docs >= 2
)
-- DIGDAG_INSERT_LINE
select
  docid,
  collect_list(feature(translate(word,':','\;'),tfidf)) as features
from
  tfidf
group by
  docid
CLUSTER by rand(43) -- random shuffling
;