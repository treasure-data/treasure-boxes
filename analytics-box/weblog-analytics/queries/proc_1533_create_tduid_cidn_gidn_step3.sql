SELECT
  cid
  , mapped_cid1 AS mapped_cid
FROM
  tmp_cidn_gidn_step2
UNION ALL
SELECT
  cid
  , mapped_cid2 AS mapped_cid
FROM
  tmp_cidn_gidn_step2
WHERE
  mapped_cid2 IS NOT NULL
