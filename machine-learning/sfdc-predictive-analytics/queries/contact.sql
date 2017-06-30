WITH contact_with_email_domain AS (
  SELECT
    *,
    SPLIT(email, '@')[2] AS email_domain
  FROM
    ${source}.contact
)
SELECT
  C.id,
  C.accountid,
  C.ownerid,
  C.title,
  C.name,
  COALESCE(regexp_replace(lower(leadsource), '[^0-9a-zA-Z]', ''), 'other') AS leadsource, -- use normalized text
  IF(
    COALESCE(C.phone, C.mobilephone, C.homephone, C.otherphone, C.assistantphone) IS NULL,
    0,
    1
  ) AS has_phone_number,
  IF(D.domain IS NULL, 0, 1) AS is_free_email
FROM contact_with_email_domain C LEFT
JOIN -- manually prepared by importing: https://github.com/willwhite/freemail/blob/master/data/free.txt
  free_domain D
  ON C.email_domain = D.domain
;
