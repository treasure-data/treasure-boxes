---
name: CampaignDetails_Spec
---

# Report Specification: Campaign Details

## 1. Report Overview
- purpose: "To provide comprehensive performance analysis for a single campaign or journey, including KPIs, trends, and email title breakdown."
- source_tables:
    - "email_events"
    - "revenue_table"

## 2. Filters
- filter:
    - id: "campaign_id"
      type: "string"
      required: true
      exclusive_with: "journey_id"
- filter:
    - id: "journey_id"
      type: "string"
      required: true
      exclusive_with: "campaign_id"
- filter_notes: "A campaign_id or journey_id is required. When one of these IDs is provided, a date range is NOT required. The report should run on all available data for that ID."
- notes: "Timestamp parsing: event_timestamp is ISO8601 format (use from_iso8601_timestamp(event_timestamp)). conversion_timestamp can be cast directly (use CAST(conversion_timestamp AS TIMESTAMP))."

## 3. Important Notes on Metrics

### Unique Count vs Total Count
- **Unique counts** (primary metrics): Use `COUNT(DISTINCT message_id)` to count each message only once, regardless of how many times it was opened/clicked.
- **Total counts** (supplementary information): Use `COUNT(*)` to count all events, including multiple opens/clicks of the same message.
- **Rate calculations**: All rates MUST use unique counts to avoid inflated metrics (industry standard).

### Identifier Standard
- Use `message_id` (Amazon SES unique message ID) for DISTINCT aggregations.
- This ensures consistency with Email Delivery Reports and industry best practices.

### Time Granularity (for trend components)

**CRITICAL: Timestamp Parsing**
- event_timestamp is stored in ISO8601 format. Use `from_iso8601_timestamp(event_timestamp)` to parse.
- conversion_timestamp can be cast directly. Use `CAST(conversion_timestamp AS TIMESTAMP)`.
- Example for date truncation: `DATE_TRUNC('day', from_iso8601_timestamp(event_timestamp))` for email events, `DATE_TRUNC('day', CAST(conversion_timestamp AS TIMESTAMP))` for revenue_table.

The SQL agent must dynamically set the time grain based on the total date range of available data for the specified campaign_id or journey_id:
- **<=20 days**: daily granularity
- **21-89 days**: weekly granularity (starting Monday)
- **>=90 days**: monthly granularity

This ensures optimal visualization density and performance.

## 4. Component Definitions

### Component 1: Engagement KPIs
- component:
    - component_id: "kpi_summary_engagement"
    - component_type: "kpi_card_group"
    - title: "Engagement KPIs for {name} ({id})"
    - source_tables: ["email_events"]
    - metrics:
        - { metric_id: "sends", display_name: "Sends", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Send'", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Delivery'", format: "integer" }
        - { metric_id: "unique_opens", display_name: "Unique Opens", calculation: "COUNT(DISTINCT message_id) FROM email_events WHERE event_type = 'Open'", format: "integer", visual_priority: "primary" }
        - { metric_id: "total_opens", display_name: "Total Opens", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Open'", format: "integer", visual_priority: "tertiary", display_note: "Supplementary information" }
        - { metric_id: "unique_open_rate", display_name: "Unique Open Rate", calculation: "(COUNT(DISTINCT message_id) WHERE event_type = 'Open') / (COUNT(*) WHERE event_type = 'Delivery')", format: "percentage", visual_priority: "primary" }
        - { metric_id: "unique_clicks", display_name: "Unique Clicks", calculation: "COUNT(DISTINCT message_id) FROM email_events WHERE event_type = 'Click'", format: "integer", visual_priority: "primary" }
        - { metric_id: "total_clicks", display_name: "Total Clicks", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Click'", format: "integer", visual_priority: "tertiary", display_note: "Supplementary information" }
        - { metric_id: "unique_click_rate", display_name: "Unique Click Rate (CTR)", calculation: "(COUNT(DISTINCT message_id) WHERE event_type = 'Click') / (COUNT(*) WHERE event_type = 'Delivery')", format: "percentage", visual_priority: "primary" }
        - { metric_id: "bounces", display_name: "Bounces", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Bounce'", format: "integer" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "(COUNT(*) WHERE event_type = 'Bounce') / (COUNT(*) WHERE event_type = 'Send')", format: "percentage" }
        - { metric_id: "unsubscribes", display_name: "Unsubscribes", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Complaint'", format: "integer" }
    - notes: |
        - Visual priority guidance:
          * "primary": Display prominently (e.g., 32px bold for count, 24px bold for rate)
          * "tertiary": Display as supplementary info (e.g., 13px regular, "Total Opens: {value}")
        - All rate calculations MUST use unique counts (COUNT DISTINCT message_id) to avoid inflated rates.

### Component 2: Revenue KPIs
- component:
    - component_id: "kpi_summary_revenue_table"
    - component_type: "kpi_card_group"
    - title: "Revenue KPIs for {name} ({id})"
    - source_tables: ["revenue_table", "email_events"]
    - display_condition: "Only show this component if filtering by campaign_id."
    - query_hints:
        - "To get revenue_table for a journey, you MUST JOIN the 'revenue_table' and 'email_events' tables on 'campaign_id'."
    - metrics:
        - { metric_id: "total_revenue_table", display_name: "Total Revenue", calculation: "SUM(total_revenue_table) from revenue_table table where attribution_type is 'direct' or 'contributed'", format: "currency", display_condition: "Only show if both direct and contributed revenue_table exist." }
        - { metric_id: "direct_revenue_table", display_name: "Direct Revenue", calculation: "SUM(total_revenue_table) from revenue_table table where attribution_type = 'direct'", format: "currency" }
        - { metric_id: "contributed_revenue_table", display_name: "Contributed Revenue", calculation: "SUM(total_revenue_table) from revenue_table table where attribution_type = 'contributed'", format: "currency" }

### Component 3: Performance by Email Title
- component:
    - component_id: "email_title_performance"
    - component_type: "table"
    - title: "Performance by Email Title"
    - source_tables: ["email_events"]
    - dimensions:
        - { id: "email_title", display_name: "Email Title" }
    - metrics:
        - { metric_id: "sends", display_name: "Sends", calculation: "COUNT(*) WHERE event_type = 'Send'", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "COUNT(*) WHERE event_type = 'Delivery'", format: "integer" }
        - { metric_id: "open_rate", display_name: "Open Rate", calculation: "(COUNT(*) WHERE event_type = 'Open') / (COUNT(*) WHERE event_type = 'Delivery')", format: "percentage" }
        - { metric_id: "ctr", display_name: "CTR (Click-Through Rate)", calculation: "(COUNT(*) WHERE event_type = 'Click') / (COUNT(*) WHERE event_type = 'Delivery')", format: "percentage" }
        - { metric_id: "bounces", display_name: "Bounces", calculation: "COUNT(*) WHERE event_type = 'Bounce'", format: "integer" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "(COUNT(*) WHERE event_type = 'Bounce') / (COUNT(*) WHERE event_type = 'Send')", format: "percentage" }
        - { metric_id: "unsubscribes", display_name: "Unsubscribes", calculation: "COUNT(*) WHERE event_type = 'Complaint'", format: "integer" }
    - sort_order: "sends DESC, email_title ASC"
    - notes: |
        - Query Construction:
          1. GROUP BY email_title directly from email_events table
          2. Filter by campaign_id or journey_id
          3. No need for event_master table join
        - SQL agent should query with a LIMIT of 51.
        - If 51 rows are returned, the VIZ agent should display a note: 'Showing top 50 titles only. There may be additional titles not displayed.'
        - Display the first 50 rows only.

### Component 4: Engagement Count Trend
- component:
    - component_id: "engagement_count_trend"
    - component_type: "line_chart"
    - title: "Engagement Trend (Counts)"
    - source_tables: ["email_events"]
    - y_axis_shared: true
    - visualization_hint: "mode: 'lines+markers'"
    - metrics:
        - { metric_id: "sends", display_name: "Sends", calculation: "COUNT(CASE WHEN event_type='Send' THEN 1 END)", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "COUNT(CASE WHEN event_type='Delivery' THEN 1 END)", format: "integer" }
        - { metric_id: "unique_opens", display_name: "Unique Opens", calculation: "COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END)", format: "integer", visual_priority: "primary" }
        - { metric_id: "unique_clicks", display_name: "Unique Clicks", calculation: "COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END)", format: "integer", visual_priority: "primary" }
        - { metric_id: "bounce_count", display_name: "Bounces", calculation: "COUNT(CASE WHEN event_type='Bounce' THEN 1 END)", format: "integer" }
        - { metric_id: "complaint_count", display_name: "Complaints", calculation: "COUNT(CASE WHEN event_type='Complaint' THEN 1 END)", format: "integer" }
    - notes: |
        - This component is based on the 'event_timestamp' column.
        - Zero-padding is NOT required.
        - Time granularity is determined by the total date range of the campaign/journey data (see Section 3).
        - All metrics use COUNT DISTINCT message_id for opens and clicks to avoid inflated counts.

### Component 5: Conversions and Revenue Trend
- component:
    - component_id: "conversions_trend"
    - component_type: "line_chart"
    - title: "Conversions & Revenue Trend"
    - source_tables: ["revenue_table", "email_events"]
    - y_axis_shared: false
    - visualization_hint: "mode: 'lines+markers', dual y-axis (left: count, right: currency)"
    - display_condition: "Only show if filtering by campaign_id."
    - metrics:
        - { metric_id: "conversions", display_name: "Conversions", calculation: "COUNT(DISTINCT conversion_id) FROM revenue_table", format: "integer", y_axis: "left" }
        - { metric_id: "direct_revenue_table", display_name: "Direct Revenue", calculation: "SUM(total_revenue_table) FROM revenue_table WHERE attribution_type = 'direct'", format: "currency", y_axis: "right" }
        - { metric_id: "contributed_revenue_table", display_name: "Contributed Revenue", calculation: "SUM(total_revenue_table) FROM revenue_table WHERE attribution_type = 'contributed'", format: "currency", y_axis: "right" }
        - { metric_id: "total_revenue_table", display_name: "Total Revenue", calculation: "SUM(total_revenue_table) FROM revenue_table WHERE attribution_type IN ('direct', 'contributed')", format: "currency", y_axis: "right" }
    - notes: |
        - This component is based on the 'conversion_timestamp' column.
        - Zero-padding is NOT required.
        - Time granularity is determined by the total date range of the campaign/journey data (see Section 3).
        - Use dual y-axis: left for count metrics (conversions), right for currency metrics (revenue_table).
        - This component helps identify day-of-week patterns and campaign timing effects.

## 5. Component Rendering Order

The final output should render components in the following order:

1. Title
2. Summary (data-driven insights)
3. kpi_summary_engagement
4. kpi_summary_revenue_table (if campaign_id and data exists)
5. engagement_count_trend
6. conversions_trend (if campaign_id and data exists)
7. email_title_performance

