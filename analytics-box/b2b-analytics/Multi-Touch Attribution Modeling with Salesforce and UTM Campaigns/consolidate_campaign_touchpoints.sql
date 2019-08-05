DROP TABLE IF EXISTS consolidated_campaign_touchpoints;
CREATE TABLE consolidated_campaign_touchpoints AS

--Salesforce
SELECT
  campaignmember.leadorcontactid,
  campaign.name as touchpoint_name,
  campaign.id as touchpoint_id,
  campaign.CHANGE_ME_vendor_name as touchpoint_source,
  TD_TIME_PARSE(campaignmember.createddate) as touchpoint_time,
  campaign.type as touchpoint_type,
  TD_TIME_PARSE(campaign.startdate) as touchpoint_startdate
FROM 
  CHANGE_ME_SFDC_campaign_table
JOIN
 SFDC.campaignmember
 on campaign.id = campaignmember.campaignid
WHERE 
  campaignmember.hasresponded = 1

UNION All

--UTM Parameters
SELECT
  A.CHANGE_ME_sfdc_id as leadorcontactid,
  B.CHANGE_ME_utm_campaign as touchpoint_name,
  NULL as touchpoint_id, 
  B.CHANGE_ME_utm_source as touchpoint_source,
  B.CHANGE_ME_time as touchpoint_time,
  B.CHANGE_ME_utm_medium as touchpoint_type,
  Min(B.time) OVER (Partition BY B.CHANGE_ME_utm_campaign) as touchpoint_startdate
FROM
  CHANGE_ME_id_unification_table A
JOIN
  CHANGE_ME_pageviews_with_utm_parameters B
ON 
  B.CHANGE_ME_td_global_id = A.CHANGE_ME_td_global_id
WHERE 
  B.CHANGE_ME_utm_source is not NULL 
  AND A.CHANGE_ME_sfdc_id is NOT NULL 