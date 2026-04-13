# ROI Reporting Agent

## Overview

This agent generates ROI (Return on Investment) reports for Treasure Data's Engage service. It autonomously analyzes campaign performance data, executes SQL queries against Trino, and produces interactive dashboards with visualizations and insights.

Two report types are supported:
- **Overall Summary Report**: High-level KPIs, trends, and campaign/journey performance over a specified period
- **Campaign Detail Report**: Detailed analysis for a specific campaign or journey, including revenue attribution

## Features

- Automated SQL query generation and execution
- Interactive visualizations with Plotly
- Multilingual support (English/Japanese)
- Multi-currency support (USD/JPY)
- KPI cards with engagement and revenue metrics
- Time-series trend analysis with dual-axis charts
- Campaign/journey performance tables with revenue attribution
- Graceful degradation when components fail

## Files

| File | Description |
|---|---|
| `system_prompt.md` | Agent system prompt — paste into System Prompt field |
| `knowledge_base_overall_summary.md` | Report spec for Overall Summary — register as Text KB named `OverallSummary_Spec` |
| `knowledge_base_campaign_details.md` | Report spec for Campaign Details — register as Text KB named `CampaignDetails_Spec` |
| `tools.yml` | All tool configurations — reference when configuring agent tools |
| `forms/td_managed_overall_summary.yml` | Form interface for Overall Summary report |
| `forms/td_managed_campaign_details.yml` | Form interface for Campaign Details report |

## Prerequisites

### Data Preparation

Before using this agent, you need to prepare the required database tables. The `roi_reporting` workflow in the treasure-boxes repository provides a reference implementation for creating these tables.

### Required Database Tables

The agent requires the following tables in the `engage_roi_reporting` database:

| Table | Description | Key Columns |
|---|---|---|
| `daily_summary` | Daily aggregated performance metrics | `summary_date`, `campaign_id`, `journey_id`, `total_sends`, `total_deliveries`, `total_opens`, `total_clicks`, `total_conversions`, `total_revenue_direct`, `total_revenue_contributed` |
| `events_master` | Campaign/journey metadata | `campaign_id`, `journey_id`, `campaign_name`, `journey_name` |
| `email_events` | Email event logs | `event_timestamp`, `event_type`, `message_id`, `campaign_id`, `journey_id`, `email_title` |
| `revenue_table` | Revenue attribution data | `conversion_timestamp`, `conversion_id`, `campaign_id`, `total_revenue`, `attribution_type` |

### Data Schema Requirements

**daily_summary table:**
- `summary_date` (varchar): Date in 'YYYY-MM-DD' format
- `campaign_id`, `journey_id` (varchar): Identifiers
- `total_sends`, `total_deliveries`, `total_opens`, `total_clicks`, `total_conversions` (integer): Event counts
- `total_hard_bounces`, `total_soft_bounces`, `total_unsubscribes` (integer): Negative event counts
- `total_revenue_direct`, `total_revenue_contributed` (double): Revenue amounts

**email_events table:**
- `event_timestamp` (varchar): Timestamp in '%Y-%m-%d %H:%i:%s.%f' format
- `event_type` (varchar): 'Send', 'Delivery', 'Open', 'Click', 'Bounce', 'Complaint'
- `message_id` (varchar): Unique message identifier
- `email_title` (varchar): Email subject line

**revenue table:**
- `conversion_timestamp` (varchar): Timestamp in '%Y-%m-%d %H:%i:%s.%f' format
- `attribution_type` (varchar): 'direct' or 'contributed'
- `total_revenue` (double): Revenue amount

## Setup Instructions

**IMPORTANT**: The `tdx agent push` command currently creates ONLY the agent resource itself. Knowledge Bases, Tools, Outputs, and Form Interfaces must be configured separately via LLM API or the AI Agent Foundry UI.

### Option A: LLM API Setup (Recommended for Complete Setup)

For a fully automated setup including all components, use the LLM API approach:

**Step 1: Create Project**
```bash
tdx llm project create "ROI Reporting Agent"
```

**Step 2-6: Use LLM API**

Use Python scripts to create the agent and all resources via LLM API. This ensures:
- ✅ Agent core attributes (name, model, system prompt)
- ✅ Knowledge Bases (Text KBs and Database KB)
- ✅ Tools and Outputs configuration
- ✅ Form Interfaces

Reference implementation: See the `/llm-api-setup` skill documentation for complete workflow and Python script templates.

**Key points:**
- Use `POST /api/agents` to create the agent with core attributes
- Use `POST /api/text_knowledge_bases` for Text KBs
- Use `POST /api/knowledge_bases` for Database KB
- Use `PATCH /api/agents/{id}` to configure tools and outputs
- Use `POST /api/form_interfaces` for form interfaces
- Verify all components after setup

### Option B: CLI + Manual Configuration (Partial Automation)

```bash
# 1. Clone or download this directory
# 2. Edit tools.yml and replace <DATABASE_NAME> with your actual database name
# 3. Create project and agent:
tdx llm project create "ROI Reporting Agent"
tdx agent push . -f
```

**Note**: `tdx agent push` creates only the agent itself. You must manually configure:
- Knowledge Bases (via UI or LLM API)
- Tools and Outputs (via LLM API)
- Form Interfaces (via LLM API)

### Option C: Manual (AI Agent Foundry UI)

#### 1. Create Project
Create a new project named **`ROI Reporting Agent`** in AI Agent Foundry.

#### 2. Register Database as Knowledge Base
- Type: **Database**
- Select your ROI reporting database (containing daily_summary, email_events, revenue tables)

#### 3. Register Report Specs as Text Knowledge Bases

**KB 1:**
- Type: **Text**, Name: `OverallSummary_Spec`
- Content: paste from `knowledge_base_overall_summary.md`

**KB 2:**
- Type: **Text**, Name: `CampaignDetails_Spec`
- Content: paste from `knowledge_base_campaign_details.md`

#### 4. Create Agent
- Name: **`Dashboard Viz`**
- System Prompt: paste from `system_prompt.md`
- Model: Claude 4.5 Sonnet
- Max tool iterations: 4
- Temperature: 0

#### 5. Configure Tools
See **[tools.yml](./tools.yml)** for all tool names, descriptions, and settings.

#### 6. Register Form Interfaces (when API available)
- Overall Summary: `forms/td_managed_overall_summary.yml`
- Campaign Details: `forms/td_managed_campaign_details.yml`

## Usage

### Overall Summary Report

```
Create dashboard with following conditions:
- Report_id: 1.Overall Summary
- Start Date: 2025-01-01
- End Date: 2025-01-31
- Timezone: UTC
- Language: English
- Currency: USD
```

```
以下の条件でダッシュボードを作成してください:
- Report_id: 1.Overall Summary
- Start Date: 2024-12-01
- End Date: 2024-12-31
- Timezone: Asia/Tokyo
- Language: Japanese
- Currency: JPY
```

**Parameters:**
- `Start_date`, `End_date` (required): Date range in 'YYYY-MM-DD' format (max 365 days)
- `Language` (required): 'English' or 'Japanese'
- `Currency` (required): 'USD' or 'JPY'
- `Timezone` (optional): Defaults to UTC

### Campaign Detail Report

```
Create dashboard with following conditions:
- Report_id: 2. Campaign Summary
- Campaign_id: ABC123
- Language: English
- Currency: USD
```

```
以下の条件でダッシュボードを作成してください:
- Report_id: 2. Campaign Summary
- Journey_id: welcome-series
- Language: Japanese
- Currency: JPY
```

**Parameters:**
- `Campaign_id` or `Journey_id` (one required): Campaign or journey identifier
- `Language` (required): 'English' or 'Japanese'
- `Currency` (required): 'USD' or 'JPY'

## Report Components

### Overall Summary includes:
1. Executive Summary (data-driven insights)
2. KPI Cards — Sends, Revenue, Conversions, Deliveries, Opens, Clicks, Bounces, Unsubscribes
3. Campaign Performance Table (top 5 by revenue)
4. Journey Performance Table (top 5 by revenue)
5. Performance Trend Chart (engagement and revenue)
6. Data Methodology Disclaimer

### Campaign Detail includes:
1. Executive Summary (data-driven insights)
2. Engagement KPI Cards — Sends, Deliveries, Opens, Clicks, Bounces, Unsubscribes
3. Revenue KPI Cards (campaign only) — Total/Direct/Contributed Revenue
4. Engagement Count Trend Chart
5. Conversions & Revenue Trend Chart (campaign only)
6. Performance by Email Title Table

### Auto Granularity
| Data span | Granularity |
|---|---|
| 1–20 days | Daily |
| 21–89 days | Weekly |
| 90+ days | Monthly |

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| "Missing required parameters" | Required filter not provided | Provide start_date, end_date, language, and currency for Overall Summary; campaign_id or journey_id for Campaign Details |
| "Date range exceeds 365 days" | Date range too long | Reduce date range to 365 days or less |
| No data returned | Filters don't match data | Verify campaign_id/journey_id exist; check date range; verify table names |
| Schema mismatch | Missing required columns | Verify tables contain required columns as documented in Prerequisites |

## Revenue Metrics

### Attribution Types
- **Direct Revenue**: Revenue from conversions that occurred within the attribution window after email interaction
- **Contributed Revenue**: Revenue from conversions where email interaction contributed but was not the last touch
- **Total Revenue**: Sum of Direct + Contributed Revenue

### Display Logic
- **Total Revenue** is shown when BOTH direct and contributed revenue exist
- Otherwise, only Direct and/or Contributed Revenue are shown separately

## License
This agent configuration is provided as-is for use with Treasure Data's Engage service.

## Support
This is a reference implementation. For assistance with setup and deployment, consult Treasure Data documentation or your account team.
