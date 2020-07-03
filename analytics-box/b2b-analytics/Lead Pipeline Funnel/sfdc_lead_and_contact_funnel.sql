WITH DOB AS(
  SELECT 
    lead.email,
    MIN(TD_TIME_PARSE(lead.createddate,
        'UTC')) AS created_date
  FROM
    lead
  GROUP BY
    1
  ORDER BY
    1 DESC
),


C AS(
  SELECT 
    contact.id,
    contact.name as lead_contact_name,
    contact.email,
    contact.title as job_title,
    account.name as account_name,
    account.id as account_id,
    account.CHANGE_ME_region as region,
    account.CHANGE_ME_industry as Industry,
    coalesce(contact.leadsource, 'Other') as leadsource,
    contact.status as lead_contact_status,

    COALESCE(
      DOB.created_date,
      TD_TIME_PARSE(
        contact.createddate,
        'UTC'
      )
    ) AS createddate,
    TD_TIME_PARSE(
      contact.CHANGE_ME_timestamp_raw,
      'UTC'
    ) AS timestamp_raw,
    TD_TIME_PARSE(
      contact.CHANGE_ME_timestamp_mql,
      'UTC'
    ) AS timestamp_mql,
    TD_TIME_PARSE(
      contact.CHANGE_ME_timestamp_sql,
      'UTC'
    ) AS timestamp_sql,
    TD_TIME_PARSE(
      contact.CHANGE_ME_timestamp_engaged,
      'UTC'
    ) AS timestamp_engaged,
    TD_TIME_PARSE(
      contact.CHANGE_ME_timestamp_nurture,
      'UTC'
    ) AS timestamp_nurture,
    TD_TIME_PARSE(
      contact.CHANGE_ME_timestamp_disqualified,
      'UTC'
    ) AS timestamp_disqualified,
      
      case when account.CHANGE_ME_account_tier is not null then account.id else null end as target_account_id,
      case when account.CHANGE_ME_account_tier is not null then account.name else null end as target_account_name,
      account.CHANGE_ME_account_tier as account_tier,
      account.type as account_type
  FROM
    contact LEFT
  JOIN
    account
    ON account.id = contact.accountid LEFT
  JOIN
    DOB
    ON DOB.email = contact.email
  LEFT JOIN
    opportunitycontactrole ocr
  ON
    contact.id = ocr.contactid
  LEFT JOIN
    opportunity o
  ON
    ocr.opportunityid = o.id
  LEFT JOIN
  WHERE
    contact.email not like '%CHANGE_ME_@company_domain' 
    or contact.email is NULL
  GROUP BY
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21
  ORDER BY
    1,
    2 DESC
),




L AS(
  SELECT 
    lead.id,
    lead.firstname || ' ' || lead.lastname AS lead_contact_name,
    lead.email,
    lead.job_title,
    coalesce(account.name, lead.company) as account_name,
    account.id as account_id,
    lead.CHANGE_ME_region,
    account.CHANGE_ME_industry as industry,
    coalesce(lead.leadsource, 'Other') as leadsource,
    lead.status as lead_contact_status,

    TD_TIME_PARSE(
      lead.createddate,
      'UTC'
    ) AS createddate,
    TD_TIME_PARSE(
      lead.CHANGE_ME_timestamp_raw,
        'UTC'
    ) AS timestamp_raw,
    TD_TIME_PARSE(
      lead.CHANGE_ME_timestamp_mql,
      'UTC'
    ) AS timestamp_mql,
    TD_TIME_PARSE(
      lead.CHANGE_ME_timestamp_sql,
      'UTC'
    ) AS timestamp_sql,
    TD_TIME_PARSE(
      lead.CHANGE_ME_timestamp_engaged,
      'UTC'
    ) AS timestamp_engaged,
    TD_TIME_PARSE(
      lead.CHANGE_ME_timestamp_nurture,
      'UTC'
    ) AS timestamp_nurture,
    TD_TIME_PARSE(
      lead.CHANGE_ME_timestamp_disqualified,
      'UTC'
    ) AS timestamp_disqualified,

    case when account.CHANGE_ME_account_tier is not null then account.id else null end as target_account_id,
    case when account.CHANGE_ME_account_tier is not null then account.name else null end as target_account_name,
    account.CHANGE_ME_account_tier as account_tier,
    account.type as account_type
  FROM
    lead
  Left JOIN
    account
    on coalesce(lead.CHANGE_ME_enriched_account_id = account.id
  WHERE
    lead.isconverted <> 1
    and 
    lead.email not like '%CHANGE_ME_@companydomain.com'  or lead.email is null)
  GROUP BY
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21
  ORDER BY
    1,
    2 DESC
)  

SELECT 
  'lead' AS sfdc_table_source,
  L.*
FROM
  L
UNION ALL 
SELECT 
  'contact' AS sfdc_table_source, 
  C. *
FROM
  C