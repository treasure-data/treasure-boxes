SELECT
  *
FROM
  samples s
WHERE
  -- for all contacts who are not associated with any opportunities
  opportunityid IS NULL
  AND
  -- ignore contacts who are associated with closed deal
  accountid not in (select accountid from opportunity where isclosed = 1)
;
