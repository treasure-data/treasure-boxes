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
    user.name as lead_contact_owner,
    account.name as account_name,
    account.id as account_id,
    account.${region},
    account.${industry},
    coalesce(contact.leadsource, 'Other') as leadsource,
    contact.${status} as lead_contact_status,

    COALESCE(
      DOB.created_date,
      TD_TIME_PARSE(
        contact.createddate,
        'UTC'
      )
    ) AS createddate,
    TD_TIME_PARSE(
      contact.${timestamp_raw},
      'UTC'
    ) AS timestamp_raw,
    TD_TIME_PARSE(
      contact.${timestamp_mql},
      'UTC'
    ) AS timestamp_mql,
    TD_TIME_PARSE(
      contact.${timestamp_sql},
      'UTC'
    ) AS timestamp_sql,
    TD_TIME_PARSE(
      contact.${timestamp_engaged},
      'UTC'
    ) AS timestamp_engaged,
    TD_TIME_PARSE(
      contact.${timestamp_nurture},
      'UTC'
    ) AS timestamp_nurture,
    TD_TIME_PARSE(
      contact.${timestamp_disqualified},
      'UTC'
    ) AS timestamp_disqualified,
      
      case when account.${account_tier} is not null then account.id else null end as target_account_id,
      case when account.${account_tier} is not null then account.name else null end as target_account_name,
      account.${account_tier},
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
    USER
  on
    contact.ownerid = USER.id
  WHERE
    contact.email not like '%@${company_domain}' 
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
    21,
    22
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
    user.name as lead_contact_owner,
    coalesce(account.name, lead.company) as account_name,
    account.id as account_id,
    lead.${region},
    account.${industry},
    coalesce(lead.leadsource, 'Other') as leadsource,
    lead.status as lead_contact_status,

    TD_TIME_PARSE(
      lead.createddate,
      'UTC'
    ) AS createddate,
    TD_TIME_PARSE(
      lead.${timestamp_raw},
        'UTC'
    ) AS timestamp_raw,
    TD_TIME_PARSE(
      lead.${timestamp_mql},
      'UTC'
    ) AS timestamp_mql,
    TD_TIME_PARSE(
      lead.${timestamp_sql},
      'UTC'
    ) AS timestamp_sql,
    TD_TIME_PARSE(
      lead.${timestamp_engaged},
      'UTC'
    ) AS timestamp_engaged,
    TD_TIME_PARSE(
      lead.${timestamp_nurture},
      'UTC'
    ) AS timestamp_nurture,
    TD_TIME_PARSE(
      lead.${timestamp_disqualified},
      'UTC'
    ) AS timestamp_disqualified,

    case when account.${account_tier} is not null then account.id else null end as target_account_id,
    case when account.${account_tier} is not null then account.name else null end as target_account_name,
    account.${account_tier} as account_tier,
    account.type as account_type
  FROM
    lead
  Left JOIN
    account
    on coalesce(lead.${enriched_matched_account_id} = account.id
  LEFT JOIN
    USER
  on
    lead.ownerid = USER.id
  WHERE
    lead.isconverted <> 1
    and 
    lead.email not like '%@${company_domain}'  or lead.email is null)
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
    21,
    22
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