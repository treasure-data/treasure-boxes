-- Email Events Collection Query
-- This query extracts email events from the specified domain's email events table
-- and transforms them into the format required for the Email Events table.
--
-- Parameters:
-- :domain - The domain for the email events table (e.g., "example_com")
-- :yesterday - The date to process (YYYY-MM-DD format)

SELECT
    message_id,
    timestamp AS event_timestamp,
    -- Hash email address using SHA-256
    TO_HEX(SHA256(TO_UTF8(to))) AS email_hash,
    activation_id,
    activation_name,
    campaign_id,
    journey_id,
    journey_stage_id,
    subject AS email_title,
    event_type,
    bounce_type,
    bounce_subtype,
    custom_event_id
FROM
    ${domain}.events
WHERE
    TD_TIME_RANGE(CAST(TO_UNIXTIME(from_iso8601_timestamp(timestamp)) AS BIGINT), '${yesterday}', CAST(DATE '${yesterday}' + INTERVAL '1' DAY AS VARCHAR))
