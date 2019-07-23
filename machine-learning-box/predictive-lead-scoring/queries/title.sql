WITH title_cnt AS (
  SELECT
    LOWER(title) AS title,
    COUNT(*) AS cnt
  FROM
    contact
  GROUP BY
    LOWER(title)
)
SELECT
  title,
  CONCAT_WS(',', COLLECT_SET(word)) AS words
FROM
  title_cnt t1
LATERAL VIEW
  explode(
    tokenize_ja(title) -- both of English and Japanese are tokenizable
  ) t2 AS word
WHERE
  (word == 'it' OR NOT is_stopword(word)) -- "it" is a meaningful stop word in a context of job title
  AND cnt >= 10-- only focus on frequent titles
GROUP BY
  title
