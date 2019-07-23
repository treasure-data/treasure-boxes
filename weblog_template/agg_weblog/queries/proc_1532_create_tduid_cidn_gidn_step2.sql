SELECT
  t1.cid
  , MIN(t2.cid) AS mapped_cid1
  , MIN(IF(t1.cid < t2.cid, t2.cid, NULL)) AS mapped_cid2
FROM
  tmp_cidn_gidn_step1 AS t1
  LEFT JOIN tmp_cidn_gidn_step1 AS t2 ON t1.mapped_cid = t2.cid
GROUP BY
  t1.cid
