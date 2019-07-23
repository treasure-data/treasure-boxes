SELECT
  idx,
  array_avg(u_rank) as Pu,
  array_avg(i_rank) as Qi,
  avg(u_bias) as Bu,
  avg(i_bias) as Bi
FROM (
  SELECT
    train_mf_sgd(userid, itemid, rating,
                 '-factor ${factor} -mu ${td.last_results.mu} -iter ${iter} -lambda ${lambda} -eta ${eta}') AS (idx, u_rank, i_rank, u_bias, i_bias)
  FROM training_mf
) t
GROUP BY idx
;
