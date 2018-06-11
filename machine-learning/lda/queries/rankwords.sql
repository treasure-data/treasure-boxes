WITH ranked as (
  select
    label,
    word,
    lambda,
    dense_rank() OVER (PARTITION BY label ORDER BY lambda DESC) AS rnk
  from
    lda_model
)
SELECT
  *
FROM
  ranked
WHERE
  rnk <= ${topk_rank}
ORDER BY
  label ASC, rnk ASC
;