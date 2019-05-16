WITH loop1 AS (
  SELECT
    t1.cid
    , t2.mapped_cid
  FROM
    tmp_cidn_gidn_step3 AS t1
    LEFT JOIN tmp_cidn_gidn_step3 AS t2 ON t1.mapped_cid = t2.cid
  GROUP BY
    t1.cid
    , t2.mapped_cid
)
, loop2 AS (
  SELECT
    t1.cid
    , t2.mapped_cid
  FROM
    loop1 AS t1
    LEFT JOIN tmp_cidn_gidn_step3 AS t2 ON t1.mapped_cid = t2.cid
  GROUP BY
    t1.cid
    , t2.mapped_cid
)
, loop3 AS (
  SELECT
    t1.cid
    , t2.mapped_cid
  FROM
    loop2 AS t1
    LEFT JOIN tmp_cidn_gidn_step3 AS t2 ON t1.mapped_cid = t2.cid
  GROUP BY
    t1.cid
    , t2.mapped_cid
)
, loop4 AS (
  SELECT
    t1.cid
    , t2.mapped_cid
  FROM
    loop3 AS t1
    LEFT JOIN tmp_cidn_gidn_step3 AS t2 ON t1.mapped_cid = t2.cid
  GROUP BY
    t1.cid
    , t2.mapped_cid
)

SELECT
  t1.cid
  , MIN(t2.mapped_cid) AS td_uid
FROM
  loop4 AS t1
  LEFT JOIN tmp_cidn_gidn_step3 AS t2 ON t1.mapped_cid = t2.cid
GROUP BY
  t1.cid
