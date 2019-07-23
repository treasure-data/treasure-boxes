WITH exploded as (
  select
    t1.docid,
    singularize(t2.word) as word
  from
    ${source} t1 LATERAL VIEW explode(tokenize(contents,true)) t2 as word
)
-- DIGDAG_INSERT_LINE
select
  l.docid,
  l.word
from
  exploded l
where
  l.word NOT IN (select s.word from stopwords s) AND
  NOT is_stopword(l.word) AND
  length(l.word) >= 2 AND cast(l.word AS double) IS NULL
;