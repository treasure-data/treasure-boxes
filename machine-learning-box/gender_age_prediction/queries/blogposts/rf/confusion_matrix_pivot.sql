-- DIGDAG_INSERT_LINE
WITH tmp as (
  SELECT
    actual,
	max(CASE WHEN predicted = 'F10x' THEN cnt ELSE 0 END) AS F10x,
	max(CASE WHEN predicted = 'F20x' THEN cnt ELSE 0 END) AS F20x,
	max(CASE WHEN predicted = 'F30x' THEN cnt ELSE 0 END) AS F30x,
	max(CASE WHEN predicted = 'M10x' THEN cnt ELSE 0 END) AS M10x,
	max(CASE WHEN predicted = 'M20x' THEN cnt ELSE 0 END) AS M20x,
	max(CASE WHEN predicted = 'M30x' THEN cnt ELSE 0 END) AS M30x
  FROM rf_confusion_matrix
  GROUP BY actual
)
select 
  actual,
  F10x,F20x,F30x,
  M10x,M20x,M30x
from
  tmp
order by
  actual asc
