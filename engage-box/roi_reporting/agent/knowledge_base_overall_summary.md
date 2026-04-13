# Report Specification: OverallSummary

## 1. Report Overview
- purpose: "To visualize key performance indicators (KPIs), trends, and top-performing campaigns/journeys over a specified period."
- source_tables:
    - "daily_summary"
    - "event_master" # Used for name lookups in rankings

## 2. Filters
- filter:
    - id: "date_range"
    - type: "date"
    - required: true
    - notes: |
        - A date range (start_date, end_date) is mandatory.
        - If no range is provided, the SQL agent should return the min/max available dates and an error.
        - The SQL agent will validate the range. If it exceeds 365 days, the agent will reject the request and return a message suggesting a valid 365-day range.

## 3. Important Notes on Metrics

**Note:** This section describes the calculation methodology. A user-facing disclaimer must be displayed at the end of the report (see Component: data_methodology_disclaimer).

## 4. Component Definitions
- component:
    - component_id: "kpi_summary"
    - component_type: "kpi_card_group"
    - title: "Overall Performance Summary"
    - metrics:
        - { metric_id: "sends", display_name: "Sends", calculation: "SUM(total_sends)", format: "integer" }
        - { metric_id: "total_revenue", display_name: "Total Revenue", calculation: "SUM(total_revenue_direct + total_revenue_contributed)", format: "currency", display_condition: "Show only if SUM(total_revenue_direct) > 0 AND SUM(total_revenue_contributed) > 0" }
        - { metric_id: "direct_revenue", display_name: "Direct Revenue", calculation: "SUM(total_revenue_direct)", format: "currency" }
        - { metric_id: "contributed_revenue", display_name: "Contributed Revenue", calculation: "SUM(total_revenue_contributed)", format: "currency" }
        - { metric_id: "conversions", display_name: "Conversions", calculation: "SUM(total_conversions)", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "SUM(total_deliveries)", format: "integer" }
        - { metric_id: "opens", display_name: "Opens", calculation: "SUM(total_opens)", format: "integer" }
        - { metric_id: "open_rate", display_name: "Open Rate", calculation: "SUM(total_opens) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "clicks", display_name: "Clicks", calculation: "SUM(total_clicks)", format: "integer" }
        - { metric_id: "click_rate", display_name: "Click Rate", calculation: "SUM(total_clicks) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "bounces", display_name: "Bounces", calculation: "SUM(total_hard_bounces + total_soft_bounces)", format: "integer" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "SUM(total_hard_bounces + total_soft_bounces) / SUM(total_sends)", format: "percentage" }
        - { metric_id: "unsubscribes", display_name: "Unsubscribes", calculation: "SUM(total_unsubscribes)", format: "integer" }

- component:
    - component_id: "campaign_performance_ranking"
    - component_type: "table"
    - title: "Top 5 Campaigns"
    - source_tables: ["daily_summary", "event_master"]
    - dimensions:
        - { id: "campaign_name", display_name: "Campaign Name" }
        - { id: "campaign_id", display_name: "Campaign ID" }
    - metrics:
        - { metric_id: "revenue", display_name: "Revenue", format: "currency" }
        - { metric_id: "conversions", display_name: "Conversions", calculation: "SUM(total_conversions)", format: "integer" }
        - { metric_id: "sends", display_name: "Sends", calculation: "SUM(total_sends)", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "SUM(total_deliveries)", format: "integer" }
        - { metric_id: "open_rate", display_name: "Open Rate", calculation: "SUM(total_opens) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "click_rate", display_name: "Click Rate", calculation: "SUM(total_clicks) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "SUM(total_hard_bounces + total_soft_bounces) / SUM(total_sends)", format: "percentage" }
    - orderby_clause_template: "ORDER BY SUM(total_revenue_direct + total_revenue_contributed) DESC, SUM(total_conversions) DESC, SUM(total_clicks) DESC, campaign_id DESC"
    - notes: |
        - This component ranks campaigns. The final sort order MUST use the provided 'orderby_clause_template'.
        - Date filtering MUST use the 'summary_date' column (varchar) with string-based comparison (e.g., WHERE summary_date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD').
        - The 'Revenue' column to be displayed is dynamic. The agent must construct a CASE statement to show Total, Direct, or Contributed Revenue based on the rules previously discussed.

- component:
    - component_id: "journey_performance_ranking"
    - component_type: "table"
    - title: "Top 5 Journeys"
    - source_tables: ["daily_summary", "event_master"]
    - dimensions:
        - { id: "journey_name", display_name: "Journey Name" }
        - { id: "journey_id", display_name: "Journey ID" }
    - metrics:
        - { metric_id: "revenue", display_name: "Revenue", format: "currency" }
        - { metric_id: "conversions", display_name: "Conversions", calculation: "SUM(total_conversions)", format: "integer" }
        - { metric_id: "sends", display_name: "Sends", calculation: "SUM(total_sends)", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "SUM(total_deliveries)", format: "integer" }
        - { metric_id: "open_rate", display_name: "Open Rate", calculation: "SUM(total_opens) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "click_rate", display_name: "Click Rate", calculation: "SUM(total_clicks) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "SUM(total_hard_bounces + total_soft_bounces) / SUM(total_sends)", format: "percentage" }
    - orderby_clause_template: "ORDER BY SUM(total_revenue_direct + total_revenue_contributed) DESC, SUM(total_conversions) DESC, SUM(total_clicks) DESC, journey_id DESC"
    - notes: |
        - This component ranks journeys. The final sort order MUST use the provided 'orderby_clause_template'.
        - Date filtering MUST use the 'summary_date' column (varchar) with string-based comparison (e.g., WHERE summary_date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD').
        - The 'Revenue' column to be displayed is dynamic. The agent must construct a CASE statement to show Total, Direct, or Contributed Revenue based on the rules previously discussed.

- component:
    - component_id: "performance_trend"
    - component_type: "trend_chart"
    - title: "Performance Trend"
    - tabs:
        - tab_name: "Engagement"
          metrics:
            - { metric_id: "sends", display_name: "Sends", calculation: "SUM(total_sends)" }
            - { metric_id: "deliveries", display_name: "Deliveries", calculation: "SUM(total_deliveries)" }
            - { metric_id: "clicks", display_name: "Clicks", calculation: "SUM(total_clicks)" }
        - tab_name: "Revenue"
          metrics:
            - { metric_id: "revenue", display_name: "Revenue", calculation: "SUM(total_revenue_direct + total_revenue_contributed)" }
          display_condition: "Show tab only if total revenue for the period > 0"
    - notes: |
        - This component uses the 'summary_date' (varchar) column. For date functions like date_trunc, it MUST be converted using CAST(summary_date AS DATE).
        - The SQL agent must dynamically set the time grain based on the length of the date range:
          * <=20 days: daily
          * 21-89 days: weekly (starting Monday)
          * >=90 days: monthly
        - The agent must perform zero-padding to ensure a continuous time series.

- component:
    - component_id: "data_methodology_disclaimer"
    - component_type: "text_note"
    - title: "Data Aggregation Methodology"
    - content: |
        Note: The open rate and click rate in this report are calculated based on total event counts from the daily_summary table.
        When the same email is opened or clicked multiple times, each event is counted separately.
        This may result in rates appearing higher than unique open/click rates.

        For more detailed analysis with unique count-based metrics, please refer to the Campaign Details report.
    - display_condition: "ALWAYS - This component MUST be displayed at the end of every report."
    - notes: |
        - CRITICAL: This disclaimer MUST always be rendered at the very end of the report, after all other components.
        - This is not optional - it must appear in every OverallSummary report regardless of data or filters.
        - Rendering style: Plain text only, no borders, no background color, no box shadow, no bold text.
        - Use regular font weight (not bold), normal font size (14-16px).
        - Background color: transparent or same as page background (white/light gray).
        - No visual highlighting or emphasis - this should blend into the page as simple footer text.

## 5. Component Rendering Order

The final output MUST render components in the following order:

1. Report Title
2. Summary (data-driven insights)
3. kpi_summary
4. campaign_performance_ranking
5. journey_performance_ranking
6. performance_trend
7. **data_methodology_disclaimer** ← MUST BE LAST

**IMPORTANT:** The data_methodology_disclaimer component MUST always appear at the very end of the report, regardless of other component rendering or data availability.
