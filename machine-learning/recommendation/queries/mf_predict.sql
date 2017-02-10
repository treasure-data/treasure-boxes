SELECT
    t2.actual,
    mf_predict(t2.Pu, p2.Qi, t2.Bu, p2.Bi, ${td.last_results.mu}) as predicted
FROM (
    SELECT
      t1.userid,
      t1.itemid,
      t1.rating as actual,
      p1.Pu,
      p1.Bu
    FROM
      testing_mf t1 LEFT OUTER JOIN mf_model p1
      ON (t1.userid = p1.idx)
) t2
LEFT OUTER JOIN mf_model p2
ON (t2.itemid = p2.idx)
;
