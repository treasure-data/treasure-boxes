-- DIGDAG_INSERT_LINE
WITH tmp as (
  SELECT
    actual,
	max(CASE WHEN predicted = 'F1x' THEN cnt ELSE 0 END) AS F1x,
	max(CASE WHEN predicted = 'F2x' THEN cnt ELSE 0 END) AS F2x,
	max(CASE WHEN predicted = 'F3x' THEN cnt ELSE 0 END) AS F3x,
	max(CASE WHEN predicted = 'M1x' THEN cnt ELSE 0 END) AS M1x,
	max(CASE WHEN predicted = 'M2x' THEN cnt ELSE 0 END) AS M2x,
	max(CASE WHEN predicted = 'M3x' THEN cnt ELSE 0 END) AS M3x
  FROM rf_confusion_matrix
  GROUP BY actual
)
select 
  actual,
  F1x,F2x,F3x,
  M1x,M2x,M3x
from
  tmp
order by
  actual asc
