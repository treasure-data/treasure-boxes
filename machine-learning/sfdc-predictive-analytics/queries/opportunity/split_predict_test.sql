SELECT
  *
FROM
  samples
WHERE -- for primary contact's unclosed opportunity
  opportunityid IS NOT NULL AND is_closed = 0 AND is_primary = 1
;
