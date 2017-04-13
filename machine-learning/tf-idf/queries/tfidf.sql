WITH excluded_stopwords AS(
  select
    *
  from
    exploded t
  where
    t.word NOT IN (
      select s.word from ${stopwords} s
    )
),
tf AS(
  select
    docid, 
    word,
    freq
  from (
    select
      docid,
      tf(word) as word2freq
    from
      excluded_stopwords
    group by
      docid
  ) t 
  LATERAL VIEW explode(word2freq) t2 as word, freq
),
df AS(
  select
    word, 
    count(distinct docid) docs
  from
    excluded_stopwords
  group by
    word
)
-- DIGDAG_INSERT_LINE
select
  tf.docid,
  tf.word, 
  -- tf.freq * (log(10, CAST(${td.last_results.n_docs} as FLOAT)/max2(1,df.docs)) + 1.0) as tfidf
  tfidf(tf.freq, df.docs, ${td.last_results.n_docs}) as tfidf
from
  tf 
  JOIN df ON (tf.word = df.word)
order by 
  tfidf desc
