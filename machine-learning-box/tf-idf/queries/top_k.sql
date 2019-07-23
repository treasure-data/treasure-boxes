WITH multiwords_list AS (
  select
    word,
    count(distinct docid) as cnt
  from
    tfidf
  group by
    word
  having
    cnt >= 2 -- at least two occurrence in docs
),
limitwords_tfidf AS (
  select
    t.docid, t.word, t.tfidf
  from
    tfidf t
    LEFT SEMI JOIN multiwords_list l ON (t.word = l.word)
),
topk AS (
  select
    each_top_k(${k}, docid, tfidf, docid, word)
      as (rank, tfidf, docid, word)
  from(
    select
      docid, word, tfidf
    from
      limitwords_tfidf
    cluster by
      docid
  ) t
)
-- DIGDAG_INSERT_LINE
select
  docid,
  map_keys(to_ordered_map(word, tfidf)) as keywords
from
  topk
group by
  docid
