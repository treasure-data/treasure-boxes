SELECT
  A.id,
  LOWER(COALESCE(A.billingcountry, '[[Unknown]]')) AS country,
  LOWER(COALESCE(A.industry, 'Other')) AS industry,
  A.name,
  CAST(A.annualrevenue AS DOUBLE) AS annualrevenue,
  A.numberofemployees
FROM
  ${source}.account A
