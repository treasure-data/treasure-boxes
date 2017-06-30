-- get responses from opportunity data
SELECT
  id,
  accountid,
  ownerid,

  isclosed,
  iswon,

  -- [classification]
  -- 2.0-6.0 (pipeline-won) => positive
  -- otherwise (including 7.0 i.e., lost opportunity) => negative
  opportunity_stage

  -- [regression]
  -- if you are planning to launch regression, real-valued columns are expected e.g. MRR forecasting
FROM (
  SELECT
    *,
    CAST(SPLIT(stagename, ' ')[1] AS DOUBLE) AS opportunity_stage
  FROM
    ${source}.opportunity
)
;
