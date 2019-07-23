WITH contact_opp_contact_role AS (
  SELECT
    C.id,
    C.accountid AS contact_accountid,
    C.ownerid AS contact_ownerid,
    C.title,
    C.name AS contact_name,
    C.leadsource,
    C.has_phone_number,
    C.is_free_email,

    -- might be NULL if contact is not associated with any opportunities
    OCR.opportunityid,
    OCR.isprimary
  FROM
    contact C LEFT
  JOIN -- if a contact is associated with opportunity, get its opportunityid
    ${source}.opportunitycontactrole OCR
    ON C.id = OCR.contactid
),
contact_opp AS (
  SELECT
    C.id,
    C.title,
    C.contact_name,
    C.leadsource,
    C.has_phone_number,
    C.is_free_email,
    C.opportunityid,
    C.isprimary AS is_primary,

    COALESCE(O.ownerid, C.contact_ownerid) AS ownerid,

    -- if account is associated with opportunity, using opportunity's accountid is more reliable
    COALESCE(O.accountid, C.contact_accountid) AS accountid,

    COALESCE(O.opportunity_stage, 0) AS opportunity_stage,
    COALESCE(O.iswon, 0) AS is_won,
    COALESCE(O.isclosed, 0) AS is_closed
  FROM
    contact_opp_contact_role C LEFT
  JOIN
    opportunity O
    ON C.opportunityid = O.id
)
SELECT
  C.*,
  A.country,
  A.industry,
  A.name AS account_name,
  A.annualrevenue,
  A.numberofemployees,
  U.alias AS owner
FROM
  contact_opp C LEFT
JOIN
  account A
  ON C.accountid = A.id LEFT
JOIN
  ${source}.user U
  ON C.ownerid = U.id
;
