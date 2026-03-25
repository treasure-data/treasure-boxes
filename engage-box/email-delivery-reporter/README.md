# Email Delivery Reporter Agent

## Overview

This agent generates email delivery reports for Treasure Data's Engage service. It autonomously analyzes email delivery logs from PlazmaDB, executes SQL queries against Trino, and produces interactive dashboards with visualizations and insights.

The agent can creates either two types of reports:
- **Overall Summary Report**: High-level KPIs, trends, and campaign/journey performance over a period
- **Campaign Detail Report**: Detailed analysis for a specific campaign, journey, or subject filter

## Features

- Automated SQL query generation and execution
- Interactive visualizations
- Multilingual support (English/Japanese)
- KPI cards with engagement and quality metrics
- Time-series trend analysis with dual-axis charts
- Campaigns/journeys/subjects performance tables
- Graceful degradation when components fail

## Prerequisites

### Required PlazmaDB Database

This agent requires a PlazmaDB database containing Engage email delivery logs.

**IMPORTANT**: The database name follows a specific pattern:
```
delivery_email_<maildomain>
```

Where `<maildomain>` is your email domain with dots (`.`) replaced by underscores (`_`).

**Examples:**
- Email domain: `example.com` → Database: `delivery_email_example_com`
- Email domain: `my-company.co.jp` → Database: `delivery_email_my_company_co_jp`

**Note**: Each user's database name will be different based on their email domain. You must ensure the correct database is registered as a knowledge base in your project before using this agent.

### Required Tables

The database must contain the following tables:

1. **events** (or alias: email_events)
   - Contains email event logs: Send, Delivery, Open, Click, Bounce, Complaint, DeliveryDelay
   - Key columns: `time`, `timestamp`, `event_type`, `email_sender_id`, `email_template_id`, `subject`, `custom_event_id`, `test_mode`, `message_id`, `campaign_id`, `journey_id`

2. **error_events**
   - Contains pre-send failures (rendering errors, runtime errors)
   - Key columns: `timestamp`, `error_type`, `error_message`, `custom_event_id`

3. **subscription_events** (or alias: email_subscription_events)
   - Contains opt-out/unsubscribe events
   - Key columns: `profile_identifier_value`, `campaign_id`, `campaign_name`, `action`, `action_source`, `received_time`, `time`

## Setup Instructions

### 1. Register PlazmaDB Database as Knowledge Base

1. Create project in your AI Agent Foundry UI
2. Go to Knowledge Base settings
3. Add your PlazmaDB database (`delivery_email_<your_domain>`)
4. Ensure the database connection is active
5. This knowledge base will be used by `List_columns` and `Query_data_directly` tools (configured in step 4) 

### 2. Create Agent

1. Create a new Agent in your project 
2. Copy the system prompt from [system_prompt.md](./system_prompt.md) into the System Prompt field
3. Save the agent configuration

### 3. Add Report Spec as Text Knowledge Base

1. Create a new Text Knowledge Base in your project
2. Copy the content from [knowledge_base.md](./knowledge_base.md) into the knowledge base
3. Link this knowledge base to your agent (it will be accessed via the `read_report_specs` tool configured in step 4)

### 4. Configure Tools

Configure the following tools for your agent. Each tool requires specific settings as detailed below.

#### 4.1 Data Access Tools

##### List_columns
- **Function name**: `List_columns`
- **Function description**: Discover table schemas. Returns column names, types, and comments for tables in the database.
- **Target**: Knowledge Base
- **Target knowledge base**: `delivery_email_<DOMAIN_NAME>`
- **Target function**: List columns

##### Query_data_directly
- **Function name**: `Query_data_directly`
- **Function description**: Execute SQL query against Plazma DB. Max 100 rows returned. Use GROUP BY aggregations. Never SELECT *. If result contains [TRUNCATED], use OFFSET and LIMIT for pagination.
- **Target**: Knowledge Base
- **Target knowledge base**: `delivery_email_<DOMAIN_NAME>`
- **Target function**: Query data directly (Presto SQL)

##### read_report_specs
- **Function name**: `read_report_specs`
- **Function description**: Spec for Report
- **Target**: Knowledge Base
- **Target knowledge base**: Email Delivery Report Specs
- **Target function**: Read

#### 4.2 Output Tools

##### renderReactApp
- **Output name**: `renderReactApp`
- **Function name**: `renderReactApp`
- **Function description**: Generates React components with Tailwind CSS. ENVIRONMENT CONSTRAINTS: 1. Charts: react-plotly.js is the ONLY installed library. recharts is NOT installed (do not import). 2. Icons: lucide-react is NOT installed; use inline <svg> tags only. 3. UI: Static view only. NO <button> or <a> tags (no download/details actions). Single file, export default.
- **Output Type**: Artifact
- **Artifact content type**: React

##### text_in_form
- **Output name**: `text_in_form`
- **Function name**: `text_in_form`
- **Function description**: renderMarkdown Call it when you'd like to return only error message
- **Output Type**: Artifact
- **Artifact content type**: Text

##### :plotly: (new_plot)
- **Output name**: `:plotly:`
- **Function name**: `new_plot`
- **Function description**: Provide visualization for analysis result by rendering charts using Plotly.js.
  - Use the color scheme: ["B4E3E3", "ABB3DB", "D9BFDF", "F8E1B0", "8FD6D4", "828DCA", "C69ED0", "F5D389", "6AC8C6", "5867B8", "B37EC0", "F1C461", "44BAB8", "2E41A6", "8CC97E", "A05EB0"]
  - For charts with more than three categories, actively use updatemenus
  - When summarizing multiple analysis, combine relevant charts into a single dashboard using Plotly's grid layout (e.g., grid: {rows: 2, columns: 2, pattern: 'independent'}) and ensure no elements overlap
  - Prevent text overlap by:
    * Include adequate margins: {l: 80, r: 80, t: 100, b: 80}
    * For pie charts with small segments (<5%), use textinfo: 'none' and rely on legend instead of labels
    * Set minimum dashboard dimensions: height: 600, width: 1000
    * For grid layouts, use wider domain spacing with 0.1 gap: [0, 0.45] and [0.55, 1]
- **Output Type**: Custom
- **Artifact content type**:
  ```json
  {
    "type": "object",
    "properties": {
      "data": {
        "type": "array",
        "description": "Plotly.js data JSON objects",
        "items": {
          "type": "object"
        }
      },
      "layout": {
        "type": "object",
        "description": "Plotly.js layout JSON object"
      }
    },
    "required": ["data"]
  }
  ```

## Usage

### Overall Summary Report

Generate a comprehensive summary report across all campaigns and journeys.

**Required Parameters:**
- `date_range`: Start and end date for the report period
  - Format: `start_date: 'YYYY-MM-DD', end_date: 'YYYY-MM-DD'`
  - If omitted: Uses full data range from database
- `language`: Report language
  - Options: `'en'` (English) or `'ja'` (Japanese)
  - Default: `'en'`

**Optional Parameters:**
- `campaign_id`: Filter by specific campaign ID
- `journey_id`: Filter by specific journey ID
- `subject`: Filter by email subject (case-insensitive substring match)

**Example Requests:**

```
Generate an overall email delivery report for January 2025 in English.
date_range: { start_date: '2025-01-01', end_date: '2025-01-31' }
language: 'en'
```

```
2024年12月のメール配信レポートを日本語で作成してください。
date_range: { start_date: '2024-12-01', end_date: '2024-12-31' }
language: 'ja'
```

```
Show me Q4 2024 email performance for campaign ABC123.
date_range: { start_date: '2024-10-01', end_date: '2024-12-31' }
campaign_id: 'ABC123'
language: 'en'
```

The above is an example of a user prompt in a chat UI, but you can also provide functionality to users who are not familiar with user prompts by creating an input `Input form` that includes the required fields above.


### Campaign Detail Report

Generate a detailed report for a specific campaign, journey, or subject.

**Required Parameters:**
- **At least one of the following**:
  - `campaign_id`: Specific campaign identifier
  - `journey_id`: Specific journey identifier
  - `subject`: Email subject filter (case-insensitive substring)

**Optional Parameters:**
- `date_range`: Start and end date
  - If omitted: Uses full data range for the specified campaign/journey
- `language`: Report language (`'en'` or `'ja'`)
  - Default: `'en'`

**Example Requests:**

```
Create a detailed report for campaign XYZ789.
campaign_id: 'XYZ789'
language: 'en'
```

```
ジャーニーID "welcome-series" の詳細レポートを日本語で作成してください。
journey_id: 'welcome-series'
language: 'ja'
```

```
Show me all emails with "Black Friday" in the subject from November 2024.
subject: 'Black Friday'
date_range: { start_date: '2024-11-01', end_date: '2024-11-30' }
language: 'en'
```

```
Analyze campaign ABC123 during December 2024 and January 2025.
campaign_id: 'ABC123'
date_range: { start_date: '2024-12-01', end_date: '2025-01-31' }
language: 'en'
```


## Report Components

### Overall Summary Report Includes:

1. **Executive Summary**: Data-driven narrative with key insights
2. **KPI Cards**:
   - Total Sends
   - Deliveries & Delivery Rate
   - Unique Opens & Open Rate (+ Total Opens)
   - Unique Clicks & Click Rate (+ Total Clicks)
   - Bounces & Bounce Rate
   - Unsubscribes & Unsubscribe Rate
3. **Performance Trend Chart**: Dual-axis line chart showing volume and rate metrics over time
4. **Campaign Performance Table**: Top 100 campaigns by send volume
5. **Journey Performance Table**: Top 100 journeys by send volume

### Campaign Detail Report Includes:

1. **Executive Summary**: Campaign-specific insights
2. **KPI Cards**: Same metrics as Overall Summary, filtered by campaign/journey/subject
3. **Performance Trend Chart**: Campaign-specific trend over time
4. **Email Subject Performance Table**: Top 100 email subjects by send volume

## Important Notes

### Database Name Dependency

**Critical**: This agent uses dynamic database discovery and does NOT hard-code database names. The agent will:

1. Execute `SHOW SCHEMAS LIKE 'delivery_email_%'` to find your database
2. Use the first matching schema automatically
3. Return an error if no matching database is found

**Action Required**: Ensure your `delivery_email_<domain>` database is properly registered before using this agent.

### Data Granularity

Time-series charts automatically adjust granularity based on the date range:
- **1-34 days**: Daily aggregation
- **35-90 days**: Weekly aggregation
- **91+ days**: Monthly aggregation

### Table Limits

Campaign, Journey, and Subject tables show the top 100 items by send volume. If more than 100 items exist, a warning banner will be displayed.

### Metric Calculations

**Important**: All open rates and click rates use **unique counts** (1 per message_id) to avoid inflated rates. Total counts are displayed as supplementary information only.

## Troubleshooting

### "No email delivery database found"

**Cause**: The agent cannot find a database matching the pattern `delivery_email_%`

**Solution**:
1. Verify your database name follows the pattern `delivery_email_<domain>`
2. Ensure the database is registered in your Agent Framework
3. Check database connection status

### "Missing required parameters"

**Cause**: Campaign Detail Report requires at least one of {campaign_id, journey_id, subject}

**Solution**: Provide at least one identifier in your request

### No data returned

**Cause**: The specified filters may not match any data

**Solution**:
1. Verify campaign_id, journey_id, or subject values exist in your data
2. Check the date range includes the period when emails were sent
3. Try broadening the filters

## License

This agent configuration is provided as-is for use with Treasure Data's Engage service.

## Support

- This is a reference for building your own agents, no support is provided.
