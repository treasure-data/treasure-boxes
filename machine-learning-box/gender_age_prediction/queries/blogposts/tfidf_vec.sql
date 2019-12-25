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
)
-- DIGDAG_INSERT_LINE
select
  userid, 
  to_ordered_list(feature(word,bm25),bm25,'-k ${num_features}') as features,
  to_ordered_list(feature(word,tfidf),tfidf,'-k ${num_features}') as tfidf_features
--  to_ordered_list(word,bm25,'-k ${num_features}') as bm25_bow_features,
--  to_ordered_list(word,tfidf,'-k ${num_features}') as tfidf_bow_features
from 
  scores
group by
  userid
;