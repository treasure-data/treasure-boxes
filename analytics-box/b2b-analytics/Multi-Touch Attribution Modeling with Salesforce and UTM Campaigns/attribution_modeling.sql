DROP TABLE IF EXISTS multi_touch_attribution_scores;
CREATE TABLE multi_touch_attribution_scores AS


WITH multivariable_prework AS(
SELECT
  *,
  (dynamic_time_decay_number/sum_dynamic_time_decay_number) *
  CASE num_sessions
    WHEN 1 THEN 1.0
    WHEN 2 THEN 0.5
  ELSE 
    CASE session_idx
      WHEN 1 THEN 0.35
      WHEN num_sessions THEN 0.35
    ELSE (1.0-0.7)/(num_sessions-2)
    END
  END AS multivariable_number,

  SUM((dynamic_time_decay_number/sum_dynamic_time_decay_number) * 
  CASE num_sessions
    WHEN 1 THEN 1.0
    WHEN 2 THEN 0.5
  ELSE 
    CASE session_idx
      WHEN 1 THEN 0.35
      WHEN num_sessions THEN 0.35
    ELSE (1.0-0.7)/(num_sessions-2)
    END
  END) OVER (PARTITION BY opportunity_id) AS sum_of_multivariable_number
FROM
partitioned_and_indexed_campaign_touchpoints)    
    

    
--First Touch
SELECT
  session_idx,
  touchpoint_time,
  conversion_timestamp,
  touchpoint_name,
  touchpoint_id,
  touchpoint_startdate,
  opportunity_name,
  opportunity_id,
  touchpoint_type,
  touchpoint_source,
  'First Touch' AS attribution_type,
  SUM(IF(session_idx = 1, 1.0, 0)) AS conversion_value,
  SUM(IF(session_idx = 1, revenue, 0)) AS revenue_conversion_value
FROM 
  partitioned_and_indexed_campaign_touchpoints
GROUP BY 1,2,3,4,5,6,7,8,9,10,11

UNION ALL

--Last Touch
SELECT 
  session_idx,
  touchpoint_time,
  conversion_timestamp,
  touchpoint_name,
  touchpoint_id,
  touchpoint_startdate,
  opportunity_name,
  opportunity_id,
  touchpoint_type,
  touchpoint_source,
  'Last Touch' AS attribution_type,
  SUM(IF(session_idx=num_sessions, 1.0, 0)) AS conversion_value,
  SUM(IF(session_idx=num_sessions, revenue, 0)) AS revenue_conversion_value
FROM 
  partitioned_and_indexed_campaign_touchpoints
GROUP BY 1,2,3,4,5,6,7,8,9,10,11

UNION ALL

--Linear
SELECT
  session_idx,
  touchpoint_time,
  conversion_timestamp,
  touchpoint_name, 
  touchpoint_id,
  touchpoint_startdate,
  opportunity_name,
  opportunity_id,
  touchpoint_type,
  touchpoint_source,
  'Linear' AS attribution_type,
  SUM(1.0/num_sessions) AS conversion_value,
  SUM(revenue/num_sessions) AS revenue_conversion_value
FROM 
  partitioned_and_indexed_campaign_touchpoints 
GROUP BY 1,2,3,4,5,6,7,8,9,10,11

UNION ALL

--U Shaped
SELECT 
  session_idx,
  touchpoint_time,
  conversion_timestamp,
  touchpoint_name,
  touchpoint_id,
  touchpoint_startdate,
  opportunity_name,
  opportunity_id,
  touchpoint_type,
  touchpoint_source,
  'U Shaped' AS attribution_type,
  SUM(1.0*
    CASE num_sessions
      WHEN 1 THEN 1.0
      WHEN 2 THEN 0.5
    ELSE 
      CASE session_idx
        WHEN 1 THEN 0.35
        WHEN num_sessions THEN 0.35
      ELSE (1.0-0.7)/(num_sessions-2)
      END
    END
  ) AS conversion_value,

  SUM(revenue*1.0*
    CASE num_sessions
      WHEN 1 THEN 1.0
      WHEN 2 THEN 0.5
    ELSE 
      CASE session_idx
        WHEN 1 THEN 0.35
        WHEN num_sessions THEN 0.35
      ELSE (1.0-0.7)/(num_sessions-2)
      END
    END
  ) AS revenue_conversion_value

FROM 
  partitioned_and_indexed_campaign_touchpoints
GROUP BY 1,2,3,4,5,6,7,8,9,10,11

UNION ALL

--Time Decay
SELECT
  session_idx,
  touchpoint_time,
  conversion_timestamp,
  touchpoint_name,
  touchpoint_id,
  touchpoint_startdate,
  opportunity_name,
  opportunity_id,
  touchpoint_type,
  touchpoint_source,
  'Time Decay' AS attribution_type,
  SUM(1.0*time_decay_number/sum_time_decay_number) as conversion_value,
  SUM(revenue*time_decay_number/sum_time_decay_number) as revenue_conversion_value
FROM 
  partitioned_and_indexed_campaign_touchpoints
GROUP BY 1,2,3,4,5,6,7,8,9,10,11


UNION ALL

--Multi-Variable Attribution
SELECT
  session_idx,
  touchpoint_time,
  conversion_timestamp,
  touchpoint_name,
  touchpoint_id,
  touchpoint_startdate,
  opportunity_name,
  opportunity_id,
  touchpoint_type,
  touchpoint_source,
  'Multi-Variable' AS attribution_type,
  SUM(1.0*multivariable_number/sum_of_multivariable_number) AS conversion_value,
  SUM(revenue * multivariable_number/sum_of_multivariable_number) AS revenue_conversion_value
FROM 
  multivariable_prework
GROUP BY 1,2,3,4,5,6,7,8,9,10,11