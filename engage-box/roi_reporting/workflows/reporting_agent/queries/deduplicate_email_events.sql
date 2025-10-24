-- Email Events Deduplication Query using row_number()
-- This query removes duplicate entries from the temporary email events table
-- by selecting only one row per message_id (the most recent one based on event_timestamp).
--
-- Advantages over previous GROUP BY implementation:
-- 1. Selects a complete row consistently (vs. potentially mixing columns from different rows)
-- 2. Uses explicit ordering criteria for selecting which duplicate to keep
-- 3. Better data integrity by ensuring all fields come from the same record
--
-- Parameters:
-- ${td.tmp_email_events_table} - The temporary table containing collected email events

WITH ranked_events AS (
  SELECT
    message_id,
    event_timestamp,
    email_hash,
    activation_id,
    activation_name,
    campaign_id,
    journey_id,
    journey_stage_id,
    email_title,
    event_type,
    bounce_type,
    bounce_subtype,
    custom_event_id,
    ROW_NUMBER() OVER (
      PARTITION BY message_id
      ORDER BY event_timestamp DESC
    ) AS row_num
  FROM ${td.tmp_email_events_table}
)
SELECT
  message_id,
  event_timestamp,
  email_hash,
  activation_id,
  activation_name,
  campaign_id,
  journey_id,
  journey_stage_id,
  email_title,
  event_type,
  bounce_type,
  bounce_subtype,
  custom_event_id
FROM ranked_events
WHERE row_num = 1
