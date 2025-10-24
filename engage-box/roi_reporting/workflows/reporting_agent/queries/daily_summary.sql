-- Daily Summary Data Generation Query
-- This query combines data from the Email Events table, Events Master table, and Revenue table
-- to create daily summary reports.
--
-- Parameters:
-- :yesterday - The date to process (YYYY-MM-DD format)
-- :events_master_table - The Events Master table name
-- :email_events_table - The Email Events table name
-- :revenue_table - The Revenue table name

WITH email_stats AS (
    -- Calculate email metrics by campaign/journey per day
    SELECT
        CAST(CAST(DATE_TRUNC('day', from_iso8601_timestamp(event_timestamp)) AS DATE) AS VARCHAR) AS summary_date,
        COALESCE(campaign_id, '') AS campaign_id,
        COALESCE(journey_id, '') AS journey_id,
        COUNT(CASE WHEN event_type = 'Send' THEN 1 END) AS total_sends,
        COUNT(CASE WHEN event_type = 'Delivery' THEN 1 END) AS total_deliveries,
        COUNT(CASE WHEN event_type = 'Open' THEN 1 END) AS total_opens,
        COUNT(CASE WHEN event_type = 'Click' THEN 1 END) AS total_clicks,
        COUNT(CASE WHEN bounce_type = 'Permanent' THEN 1 END) AS total_hard_bounces,
        COUNT(CASE WHEN bounce_type = 'Transient' THEN 1 END) AS total_soft_bounces,
        COUNT(CASE WHEN event_type = 'Complaint' THEN 1 END) AS total_unsubscribes
    FROM
        ${email_events_table}
    WHERE
        TD_TIME_RANGE(CAST(TO_UNIXTIME(CAST(from_iso8601_timestamp(event_timestamp) AS DATE)) AS BIGINT), '${yesterday}', CAST(DATE '${yesterday}' + INTERVAL '1' DAY AS VARCHAR))
    GROUP BY
        1, 2, 3
),

revenue_stats AS (
    -- Calculate revenue metrics by campaign/journey per day
    SELECT
        CAST(CAST(DATE_TRUNC('day', CAST(conversion_timestamp AS TIMESTAMP)) AS DATE) AS VARCHAR) AS summary_date,
        COALESCE(campaign_id, '') AS campaign_id,
        '' AS journey_id, -- Assuming revenue is tracked at campaign level only for now
        SUM(CASE WHEN attribution_type = 'direct' THEN total_revenue ELSE 0 END) AS total_revenue_direct,
        SUM(total_revenue) AS total_revenue_contributed,
        COUNT(conversion_id) AS total_conversions
    FROM
        ${revenue_table}
    WHERE
        TD_TIME_RANGE(CAST(TO_UNIXTIME(CAST(conversion_timestamp AS TIMESTAMP)) AS BIGINT), '${yesterday}', CAST(DATE '${yesterday}' + INTERVAL '1' DAY AS VARCHAR))
    GROUP BY
        1, 2, 3
),

-- Add campaign and journey names from master data
master_data AS (
    SELECT
        COALESCE(campaign_id, '') AS campaign_id,
        COALESCE(campaign_name, '') AS campaign_name,
        COALESCE(journey_id, '') AS journey_id,
        COALESCE(journey_name, '') AS journey_name
    FROM
        ${events_master_table}
)

-- Combine all data to create the final daily summary
SELECT
    COALESCE(e.summary_date, r.summary_date) AS summary_date,
    COALESCE(e.campaign_id, r.campaign_id) AS campaign_id,
    m.campaign_name,
    COALESCE(e.journey_id, r.journey_id) AS journey_id,
    m.journey_name,
    COALESCE(e.total_sends, 0) AS total_sends,
    COALESCE(e.total_deliveries, 0) AS total_deliveries,
    COALESCE(e.total_opens, 0) AS total_opens,
    COALESCE(e.total_clicks, 0) AS total_clicks,
    COALESCE(e.total_hard_bounces, 0) AS total_hard_bounces,
    COALESCE(e.total_soft_bounces, 0) AS total_soft_bounces,
    COALESCE(e.total_unsubscribes, 0) AS total_unsubscribes,
    COALESCE(r.total_revenue_direct, 0) AS total_revenue_direct,
    COALESCE(r.total_revenue_contributed, 0) AS total_revenue_contributed,
    COALESCE(r.total_conversions, 0) AS total_conversions
FROM
    email_stats e
FULL OUTER JOIN
    revenue_stats r
ON
    e.summary_date = r.summary_date AND
    e.campaign_id = r.campaign_id AND
    e.journey_id = r.journey_id
LEFT JOIN
    master_data m
ON
    COALESCE(e.campaign_id, r.campaign_id) = m.campaign_id AND
    COALESCE(e.journey_id, r.journey_id) = m.journey_id
WHERE
    COALESCE(e.summary_date, r.summary_date) = '${yesterday}'
