-- @TD distribute_strategy: moderate
SELECT
  label, word, avg(lambda) as lambda
FROM (
  SELECT
    train_lda(features, '-topics ${num_topics} -iter ${iterations}') 
	  as (label, word, lambda)
  FROM
    input
) t1
GROUP BY
  label, word
;
