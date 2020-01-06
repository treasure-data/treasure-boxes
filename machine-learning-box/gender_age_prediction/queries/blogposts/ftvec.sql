-- @TD distribute_strategy: aggressive
WITH term_frequency as (
  select
    t1.userid,
    t2.word,
    t2.freq
  from (
    select
      userid,
      tf(word) as word2freq
    from
      exploded
    group by
      userid
  ) t1 
  LATERAL VIEW explode(word2freq) t2 as word, freq
),
document_frequency AS (
  select
    word,
    count(distinct userid) docs
  from
    exploded
  group by
    word
),
doc_len as (
  select 
    userid, 
    count(1) as dl,
    avg(count(1)) over () as avgdl,
    APPROX_COUNT_DISTINCT(userid) over () as total_docs
  from
    exploded
  group by
    userid
),
scores as (
  select
    tf.userid,
    tf.word,
    bm25(tf.freq, dl.dl, dl.avgdl, dl.total_docs, df.docs) as bm25,
    tfidf(tf.freq, df.docs, dl.total_docs) as tfidf
  from
    term_frequency tf
    JOIN document_frequency df ON (tf.word = df.word)
    JOIN doc_len dl ON (tf.userid = dl.userid)
  where
    df.docs >= 2
),
ftvec as (
  select
    userid,
    to_ordered_list(feature(word,cnt), value, '-k 100') as features
  from
    wordcnt
  group by
    userid
),
ages as (
  select
    userid,
    (if(gender='male','M','F') ||
    CASE
       WHEN age >= 33 THEN '3x'
       WHEN age >= 23 THEN '2x'
       ELSE '1x'
    END
    ) as gender_age
  from
    blogposts
)
-- DIGDAG_INSERT_LINE
SELECT
  l.userid,
  l.features,
  r.gender_age,
  -- random sampling
  rand(42) as rnd,
  -- stratified sampling
  count(1) over (partition by r.gender_age) as per_label_count,
  rank() over (partition by r.gender_age order by rand(41)) as rank_in_label
FROM
  ftvec l
  JOIN ages r ON (l.userid = r.userid)