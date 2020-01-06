-- DIGDAG_INSERT_LINE
WITH tmp as (
  SELECT
    actual,
	max(CASE WHEN predicted = 'F15' THEN cnt ELSE 0 END) AS F15,
	max(CASE WHEN predicted = 'F20' THEN cnt ELSE 0 END) AS F20,
	max(CASE WHEN predicted = 'F25' THEN cnt ELSE 0 END) AS F25,
	max(CASE WHEN predicted = 'F35' THEN cnt ELSE 0 END) AS F35,
	max(CASE WHEN predicted = 'F50' THEN cnt ELSE 0 END) AS F50,
	max(CASE WHEN predicted = 'M15' THEN cnt ELSE 0 END) AS M15,
	max(CASE WHEN predicted = 'M20' THEN cnt ELSE 0 END) AS M20,
	max(CASE WHEN predicted = 'M25' THEN cnt ELSE 0 END) AS M25,
	max(CASE WHEN predicted = 'M35' THEN cnt ELSE 0 END) AS M35,
	max(CASE WHEN predicted = 'M50' THEN cnt ELSE 0 END) AS M50
  FROM rf_confusion_matrix
  GROUP BY actual
)
select 
  actual,
  F15,F20,F25,F35,F50,
  M15,M20,M25,M35,M50
from
  tmp
order by
  actual asc
