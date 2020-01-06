-- @TD distribute_strategy: aggressive
-- DIGDAG_INSERT_LINE
SELECT
  userid,
  translate(r.word,':','\;') as word
FROM
  blogposts l
  LATERAL VIEW explode(
    tokenize(normalize_unicode(translate(post,':','\;'),'NFKC'),true)
  ) r as word
WHERE
  NOT is_stopword(r.word) AND
  length(r.word) >= 2 AND cast(r.word AS double) IS NULL