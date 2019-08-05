DROP TABLE IF EXISTS partitioned_and_indexed_campaign_touchpoints;
CREATE TABLE partitioned_and_indexed_campaign_touchpoints AS


WITH T0 AS (
SELECT DISTINCT
  t.touchpoint_time,
  t.touchpoint_id,
  t.touchpoint_name,
  t.touchpoint_type,
  t.touchpoint_source,
  t.touchpoint_startdate,
date_diff('second',cast(from_unixtime(t.touchpoint_time) as timestamp),cast(o.CHANGE_ME_conversion_timestamp as timestamp)) as seconds_between_touchpoint_and_conversion,
  o.name AS opportunity_name,
  o.id AS opportunity_id,
  o.type AS opportunity_type,
  o.CHANGE_ME_revenue as revenue,
  TD_TIME_PARSE(o.CHANGE_ME_conversion_timestamp) as conversion_timestamp
FROM
  consolidated_campaign_touchpoints t
JOIN
  sfdc.opportunitycontactrole ocr
  ON t.leadorcontactid = ocr.contactid
JOIN
  sfdc.opportunity o
  ON ocr.opportunityid = o.id
WHERE
t.touchpoint_time < TD_TIME_PARSE(o.CHANGE_ME_conversion_timestamp)
),

--This part only needed for Multi-Variable attribution model. Omit if not needed.
------------------------------------------------------------------------------------------------------------------------------------------
--Create 90 day windows for each touchpoint_type
T1 AS(
SELECT 
  *,
  TD_SESSIONIZE_WINDOW(touchpoint_time, 7776000) OVER (PARTITION BY touchpoint_type order by touchpoint_time asc) AS session_id
FROM 
  T0
ORDER BY touchpoint_type
),
  
  
--Get average time to conversion and standard deviation for each 90 day window according to touchpoint_type. Also get all time average and standard deviation for every touchpoint_type in case there is only 1 touchpoint of its type in a 90 day session
T2 AS(SELECT 
  *,
  AVG(IF(touchpoint_time < conversion_timestamp, seconds_between_touchpoint_and_conversion, NULL)) OVER (PARTITION BY session_id) AS average_touchpoint_to_conversion,
  STDDEV(IF(touchpoint_time < conversion_timestamp, seconds_between_touchpoint_and_conversion, NULL)) OVER (PARTITION BY session_id) AS stddev_touchpoint_to_conversion,
  AVG(IF(touchpoint_time < conversion_timestamp, seconds_between_touchpoint_and_conversion, NULL)) OVER (PARTITION BY touchpoint_type) AS all_time_average_touchpoint_to_conversion,
  STDDEV(IF(touchpoint_time < conversion_timestamp, seconds_between_touchpoint_and_conversion, NULL)) OVER (PARTITION BY touchpoint_type) AS all_time_stddev_touchpoint_to_conversion,
  COUNT(seconds_between_touchpoint_and_conversion) OVER (PARTITION BY session_id) AS conversion_session_total,
  COUNT(1) OVER (PARTITION BY touchpoint_type) AS touchpoint_total
FROM
  T1
)

--Normalize 90 day windows
,T3 AS(
SELECT
  *,
  normal_cdf(average_touchpoint_to_conversion,stddev_touchpoint_to_conversion,seconds_between_touchpoint_and_conversion) AS normalized_value,
  normal_cdf(all_time_average_touchpoint_to_conversion,all_time_stddev_touchpoint_to_conversion,seconds_between_touchpoint_and_conversion) AS all_time_normalized_value
FROM
  T2
)


--Get 50th Percentile
,T4 AS(
SELECT
  *,
  APPROX_PERCENTILE(normalized_value,0.5) OVER (PARTITION BY session_id) AS fiftieth_percentile,
  APPROX_PERCENTILE(all_time_normalized_value,0.5) OVER (PARTITION BY touchpoint_type) AS all_time_fiftieth_percentile
FROM
  T3
)
------------------------------------------------------------------------------------------------------------------------------------------
  
--Partition touchpoints by opportunity and index each touchpoint by when it occurred. "604800" (1 week) is the time it takes for a credit to be halved in the time-decay model. It can be changed to fit the organization's sales cycle.
SELECT
  *,
  POWER(2,-1*(seconds_between_touchpoint_and_conversion/604800)) AS time_decay_number,
  SUM(power(2,-1*(seconds_between_touchpoint_and_conversion/604800))) OVER (PARTITION BY opportunity_id) AS sum_time_decay_number,
  COUNT(1) OVER (PARTITION BY opportunity_id) AS num_sessions,
  ROW_NUMBER() OVER (PARTITION BY opportunity_id ORDER BY touchpoint_time) AS session_idx,

--This part is only needed for multi-variable attribution. Omit if not needed.
--************************************************************************************************************************************
  CASE 
    WHEN touchpoint_total = 1 THEN 1.0
    WHEN conversion_session_total = 1 THEN power(2,-1*(all_time_normalized_value/all_time_fiftieth_percentile))
    ELSE power(2,-1*(normalized_value/fiftieth_percentile))
    END AS dynamic_time_decay_number,

  SUM(
    CASE 
      WHEN touchpoint_total = 1 THEN 1.0
      WHEN conversion_session_total = 1 THEN power(2,-1*(all_time_normalized_value/all_time_fiftieth_percentile))
      ELSE power(2,-1*(normalized_value/fiftieth_percentile)) END
     ) OVER (PARTITION BY opportunity_id) 
      AS sum_dynamic_time_decay_number
--************************************************************************************************************************************

FROM
  T4
WHERE
  touchpoint_time < conversion_timestamp
