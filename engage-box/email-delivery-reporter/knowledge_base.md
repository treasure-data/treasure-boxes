# Email Delivery Report Specs

This document defines the report specifications for Engage Email delivery reporting.
It covers two report variants: Overall Summary and Campaign/Journey Summary.

---

## Common Terminology

**Volume Metrics:**
- `sends`: Total email send attempts (event_type = 'Send').
- `deliveries`: Successfully delivered emails (event_type = 'Delivery').
- `delivery_rate`: deliveries / sends

**Engagement Metrics (Unique-based):**
- `unique_opens`: Distinct message_id count where event_type = 'Open'
- `total_opens`: Total open event count (for reference)
- `unique_open_rate`: unique_opens / deliveries
- `unique_clicks`: Distinct message_id count where event_type = 'Click'
- `total_clicks`: Total click event count (for reference)
- `unique_click_rate`: unique_clicks / deliveries

**Quality Metrics:**
- `bounces`: Failed deliveries (event_type = 'Bounce').
- `bounce_rate`: bounces / sends
- `complaints`: Spam complaints (event_type = 'Complaint').
- `unsubscribes`: Opt-out events (rows in subscription_events where action='opt-out').
- `unsubscribe_rate`: unsubscribes / deliveries

**Important**: All open rates and click rates MUST use unique counts (1 per message_id) to avoid inflated rates. Total counts are displayed as supplementary information only.

---

## Common SQL Patterns

### Metric Aggregation from events table

```sql
SUM(CASE WHEN event_type = 'Send' THEN 1 ELSE 0 END)       -- sends
SUM(CASE WHEN event_type = 'Delivery' THEN 1 ELSE 0 END)   -- deliveries
SUM(CASE WHEN event_type = 'Open' THEN 1 ELSE 0 END)       -- total_opens
COUNT(DISTINCT CASE WHEN event_type = 'Open' THEN message_id END)  -- unique_opens
SUM(CASE WHEN event_type = 'Click' THEN 1 ELSE 0 END)      -- total_clicks
COUNT(DISTINCT CASE WHEN event_type = 'Click' THEN message_id END) -- unique_clicks
SUM(CASE WHEN event_type = 'Bounce' THEN 1 ELSE 0 END)     -- bounces
SUM(CASE WHEN event_type = 'Complaint' THEN 1 ELSE 0 END)  -- complaints
```

### Unsubscribes from subscription_events table
```sql
COUNT(*) WHERE action = 'opt-out'
```

### Rate Calculations (division safety)
```sql
CAST(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)  -- delivery_rate

CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)  -- unique_open_rate

CAST(COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)  -- unique_click_rate

CAST(SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)  -- bounce_rate

CAST(COUNT(*) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)  -- unsubscribe_rate (from subscription_events)
```

### Date Filtering
```sql
DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ')) BETWEEN DATE '{start_date}' AND DATE '{end_date}'
```

### Time Aggregation Policy
Based on the data span of `DATE(timestamp)` from email_events:

| Data Span | Granularity | date_key expression |
|-----------|-------------|---------------------|
| 1-34 days | daily | `DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ'))` |
| 35-90 days | weekly | `date_trunc('week', DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ')))` |
| 91+ days | monthly | `date_trunc('month', DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ')))` |

---

## Report Spec: DeliveryOverallSummary

### Overview
- **Purpose**: Delivery KPIs, trends, and campaign/journey lists over a period (no revenue or conversion).
- **Source tables**: events, subscription_events
- **Visual Design**: Modern, colorful cards with emoji icons, gradient backgrounds, and enhanced charts

### Filters

| Filter ID | Type | Required | Notes |
|-----------|------|----------|-------|
| date_range | date | YES | start_date and end_date mandatory. If missing: return min/max available dates and use full range. If range > 365 days: accept but warn. |
| campaign_id | string | no | Optional additional filter. Applied to all components. |
| journey_id | string | no | Optional additional filter. Applied to all components. |
| subject | string | no | Case-insensitive substring match on email subject. |

**Note**: campaign_id and journey_id are native columns in the events table.

### Components

#### Component: executive_summary
- **component_type**: text_summary
- **title**: "📊 Executive Summary"
- **content**: Data-driven narrative summary including:
  - Total period duration (in days)
  - Total sends and delivery rate
  - Engagement metrics (unique opens, total opens, unique clicks, total clicks with rates)
  - Quality metrics (bounces, complaints, unsubscribes with rates)
  - Notable patterns (e.g., bulk sends, peak periods)
- **style**:
  - White background with subtle shadow
  - 16px font size, 1.8 line height
  - Bold highlights for key numbers with color coding
  - Rounded corners (12px border radius)

#### Component: kpi_summary
- **component_type**: kpi_card_group
- **title**: "📈 Key Performance Indicators"
- **layout**: Responsive grid (auto-fit, minmax(220px, 1fr))
- **card_design**:
  - Gradient background (color + 15% opacity to white)
  - Rounded corners (12px)
  - Box shadow for depth
  - Emoji icon for each metric category
  - Primary metric: 32px bold, colored
  - Secondary metric: 24px bold, gray
  - Tertiary info: 13px, gray (for total counts)
  - Divider line between primary and secondary
  - Labels: 13px, uppercase, letter-spacing

**Metrics:**

| metric_id | display_name | emoji | calculation | format | color | card_grouping |
|-----------|--------------|-------|-------------|--------|-------|---------------|
| sends | Total Sends | 📤 | `SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END)` | integer | #44BAB8 | sends_only |
| deliveries | Delivered | ✅ | `SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END)` | integer | #44BAB8 | deliveries_with_rate |
| delivery_rate | Delivery Rate | ✅ | `CAST(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)` | percentage | #44BAB8 | deliveries_with_rate |
| unique_opens | Unique Opens | 👁️ | `COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END)` | integer | #5867B8 | opens_with_rate |
| unique_open_rate | Unique Open Rate | 👁️ | `CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage | #5867B8 | opens_with_rate |
| total_opens | Total Opens | 👁️ | `SUM(CASE WHEN event_type='Open' THEN 1 ELSE 0 END)` | integer | #5867B8 | opens_tertiary |
| unique_clicks | Unique Clicks | 🖱️ | `COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END)` | integer | #B37EC0 | clicks_with_rate |
| unique_click_rate | Unique Click Rate | 🖱️ | `CAST(COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage | #B37EC0 | clicks_with_rate |
| total_clicks | Total Clicks | 🖱️ | `SUM(CASE WHEN event_type='Click' THEN 1 ELSE 0 END)` | integer | #B37EC0 | clicks_tertiary |
| bounces | Total Bounces | ⚠️ | `SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END)` | integer | #e74c3c | bounces_with_rate |
| bounce_rate | Bounce Rate | ⚠️ | `CAST(SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)` | percentage | #e74c3c | bounces_with_rate |
| unsubscribes | Total Unsubscribes | 🚫 | `COUNT(*) FROM subscription_events WHERE action='opt-out'` | integer | #95a5a6 | unsubscribes_with_rate |
| unsubscribe_rate | Unsubscribe Rate | 🚫 | `CAST(COUNT(*) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage | #95a5a6 | unsubscribes_with_rate |

**Card Grouping Logic:**
- **Sends Card**: Shows only sends (no secondary metric)
- **Deliveries Card**: Primary = deliveries (integer), Secondary = delivery_rate (percentage)
- **Unique Opens Card**: Primary = unique_opens (integer), Secondary = unique_open_rate (percentage), Tertiary = "Total Opens: {total_opens}"
- **Unique Clicks Card**: Primary = unique_clicks (integer), Secondary = unique_click_rate (percentage), Tertiary = "Total Clicks: {total_clicks}"
- **Bounces Card**: Primary = bounces (integer), Secondary = bounce_rate (percentage)
- **Unsubscribes Card**: Primary = unsubscribes (integer), Secondary = unsubscribe_rate (percentage)

#### Component: performance_trend
- **component_type**: dual_axis_line_chart
- **title**: "📉 Monthly Performance Trend" (adjust based on granularity)
- **time_column**: date_key (derived per aggregation policy)
- **zero_padding**: required (use SEQUENCE and LEFT JOIN)
- **chart_design**:
  - Width: 1300px, Height: 650px
  - Margins: {l:80, r:100, t:60, b:80}
  - Plot background: #fafafa
  - Paper background: white
  - Grid color: #e8e8e8
  - Line width: 3px
  - Marker size: 8px
  - Fill area under sends line (tozeroy with 20% opacity)
  - Legend: horizontal, centered below chart
  - Hover mode: x unified

**Layout Config:**
- **yaxis (left)**: Volume metrics
- **yaxis2 (right)**: Rate metrics

**Metrics:**

| metric_id | display_name | calculation | axis | format | color | style |
|-----------|--------------|-------------|------|--------|-------|-------|
| sends | Sends | `SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END)` | left | integer | #44BAB8 | solid line + fill |
| deliveries | Deliveries | `SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END)` | left | integer | #8FD6D4 | solid line |
| unique_clicks | Unique Clicks | `COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END)` | left | integer | #B37EC0 | solid line |
| unique_open_rate | Unique Open Rate (%) | `CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0) * 100` | right | percentage | #F1C461 | dotted line + diamond markers |

**SQL Pattern for Trend with Zero-Padding:**

```sql
WITH date_range AS (
  SELECT
    CAST(MIN(DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ'))) AS DATE) as s,
    CAST(MAX(DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ'))) AS DATE) as e
  FROM events
  WHERE [date_filter]
),
time_series AS (
  SELECT date_trunc('month', t.dt) as month_start
  FROM date_range
  CROSS JOIN UNNEST(SEQUENCE(s, e, INTERVAL '1' DAY)) AS t(dt)
  GROUP BY date_trunc('month', t.dt)
),
monthly_metrics AS (
  SELECT
    date_trunc('month', DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ'))) as month_start,
    SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END) as sends,
    SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END) as deliveries,
    COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) as unique_opens,
    COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) as unique_clicks
  FROM events
  WHERE [date_filter]
  GROUP BY date_trunc('month', DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ')))
)
SELECT
  CAST(ts.month_start AS VARCHAR) as month_start,
  COALESCE(mm.sends, 0) as sends,
  COALESCE(mm.deliveries, 0) as deliveries,
  COALESCE(mm.unique_clicks, 0) as unique_clicks,
  CAST(COALESCE(mm.unique_opens, 0) AS DOUBLE) / NULLIF(COALESCE(mm.deliveries, 0), 0) as unique_open_rate
FROM time_series ts
LEFT JOIN monthly_metrics mm ON ts.month_start = mm.month_start
ORDER BY ts.month_start
```

#### Component: campaign_performance_list
- **component_type**: table
- **title**: "📋 All Campaigns Performance"
- **source_tables**: events (using native campaign_id and campaign_name columns)
- **dimensions**:
  - campaign_id (Campaign ID)
  - campaign_name (Campaign Name)
- **metrics**:

| metric_id | display_name | calculation | format |
|-----------|--------------|-------------|--------|
| sends | Sends | `SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END)` | integer |
| deliveries | Deliveries | `SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END)` | integer |
| unique_opens | Unique Opens | `COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END)` | integer |
| unique_open_rate | Unique Open Rate | `CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage |
| unique_click_rate | Unique Click Rate | `CAST(COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage |
| bounce_rate | Bounce Rate | `CAST(SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)` | percentage |

- **orderby_clause_template**: `ORDER BY SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END) DESC, campaign_id DESC`
- **limit**: 100
- **notes**:
  - Show top 100 campaigns ordered by sends
  - If result count = 100, execute: `SELECT COUNT(DISTINCT campaign_id) FROM events WHERE [filters] AND campaign_id IS NOT NULL`
  - If total count > 100, display warning: "⚠️ Showing top 100 of {total_count} campaigns. Results are ordered by send volume (highest first)."
  - Skip this component if no campaign_id data exists

#### Component: journey_performance_list
- **component_type**: table
- **title**: "🚀 All Journeys Performance"
- **source_tables**: events (using native journey_id column)
- **dimensions**:
  - journey_id (Journey ID)
- **metrics**: Same as campaign_performance_list
- **orderby_clause_template**: `ORDER BY SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END) DESC, journey_id DESC`
- **limit**: 100
- **notes**:
  - Show top 100 journeys ordered by sends
  - If result count = 100, execute: `SELECT COUNT(DISTINCT journey_id) FROM events WHERE [filters] AND journey_id IS NOT NULL`
  - If total count > 100, display warning: "⚠️ Showing top 100 of {total_count} journeys. Results are ordered by send volume (highest first)."
  - Skip this component if no journey_id data exists

---

## Report Spec: DeliveryCampaignSummary

### Overview
- **Purpose**: Detailed delivery performance summary for a single campaign, journey, or subject-filtered slice (no revenue).
- **Source tables**: events, subscription_events
- **Visual Design**: Same as DeliveryOverallSummary

### Filters

| Filter ID | Type | Required | Notes |
|-----------|------|----------|-------|
| campaign_id | string | no | Mutually exclusive with journey_id. |
| journey_id | string | no | Mutually exclusive with campaign_id. |
| subject | string | no | Case-insensitive substring match. |
| date_range | date | no | Optional date range filter. |

**Filter rules**: At least one of {campaign_id, journey_id, subject} is required. If multiple are provided, AND them.

### Components

#### Component: executive_summary
- **component_type**: text_summary
- **title**: "📊 Executive Summary for {name}"
- **content**: Data-driven narrative summary including:
  - Campaign/Journey/Subject identification
  - Total period duration (in days)
  - Total sends and delivery rate
  - Engagement metrics (unique opens, total opens, unique clicks, total clicks with rates)
  - Quality metrics (bounces, complaints, unsubscribes with rates)
  - Notable patterns specific to this campaign/journey

#### Component: kpi_summary_engagement
- **component_type**: kpi_card_group
- **title**: "📈 Key Performance Indicators for {name}"
- **source_tables**: events, subscription_events
- **metrics**: Same structure as DeliveryOverallSummary kpi_summary
- **notes**: All metrics filtered by campaign_id OR journey_id OR subject

#### Component: performance_trend
- **component_type**: dual_axis_line_chart
- **title**: "📉 Delivery Trend for {name}"
- **time_column**: date_key (derived per aggregation policy)
- **metrics**: Same as DeliveryOverallSummary performance_trend
- **notes**:
  - Use aggregation policy (daily/weekly/monthly) based on data span
  - Zero-padding recommended but not strictly required

#### Component: email_subject_performance_list
- **component_type**: table
- **title**: "📧 All Email Subjects Performance"
- **source_tables**: events
- **dimensions**:
  - subject (Email Subject)
  - Optionally: email_template_id
- **metrics**:

| metric_id | display_name | calculation | format |
|-----------|--------------|-------------|--------|
| sends | Sends | `SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END)` | integer |
| deliveries | Deliveries | `SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END)` | integer |
| unique_opens | Unique Opens | `COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END)` | integer |
| unique_open_rate | Unique Open Rate | `CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage |
| unique_click_rate | Unique Click Rate | `CAST(COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage |
| bounces | Bounces | `SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END)` | integer |
| bounce_rate | Bounce Rate | `CAST(SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)` | percentage |
| unsubscribes | Unsubscribes | `COUNT(*) FROM subscription_events WHERE ...` | integer |

- **orderby_clause_template**: `ORDER BY SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END) DESC, subject ASC`
- **limit**: 100
- **notes**:
  - Show top 100 subjects ordered by sends
  - If result count = 100, execute: `SELECT COUNT(DISTINCT subject) FROM events WHERE [filters]`
  - If total count > 100, display warning: "⚠️ Showing top 100 of {total_count} email subjects. Results are ordered by send volume (highest first)."
  - Use COALESCE to turn NULL into 0
  - Filter by campaign_id/journey_id/subject as specified

---

## Design System

### Color Palette
```javascript
const colors = [
  "#44BAB8",  // Teal (sends, deliveries)
  "#5867B8",  // Blue (opens)
  "#B37EC0",  // Purple (clicks)
  "#F1C461",  // Yellow (rates)
  "#8FD6D4",  // Light teal
  "#828DCA",  // Light blue
  "#C69ED0",  // Light purple
  "#F5D389",  // Light yellow
  "#e74c3c",  // Red (bounces, errors)
  "#95a5a6"   // Gray (unsubscribes)
];
```

### Typography
- **Font family**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif
- **Title**: 32px, bold (700)
- **Section headers**: 20px, semi-bold (600)
- **Card titles**: 14px, semi-bold (600), uppercase, letter-spacing 0.5px
- **Primary values**: 32px, bold
- **Secondary values**: 24px, bold
- **Tertiary info**: 13px, regular
- **Body text**: 16px, line-height 1.8
- **Labels**: 13-14px

### Spacing
- **Page padding**: 40px
- **Section margin-bottom**: 32px
- **Card gap**: 24px
- **Card padding**: 24-32px
- **Border radius**: 12px

### Shadows & Borders
- **Card shadow**: 0 4px 6px rgba(0,0,0,0.1)
- **Section shadow**: 0 2px 8px rgba(0,0,0,0.08)
- **Border**: 1px solid #e8e8e8

---

## Implementation Notes

1. **Always use unique counts for rates**: Never calculate open_rate or click_rate using total event counts
2. **Display both unique and total**: Show unique as primary metric, total as supplementary info
3. **Limited lists with warnings**: Campaign, Journey, and Subject tables show top 100 rows with warning if more exist
4. **Consistent formatting**: Use formatNumber() helper for all numeric displays
5. **Graceful degradation**: If a component has no data, skip it with a note
