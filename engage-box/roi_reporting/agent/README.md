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

## Prerequisites

### Required Tools

- `tdx` CLI (version 2026.4.55 or later)
- Git or `gh` CLI (for cloning repository)

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

## Setup Instructions

### Quick Start

```bash
# 1. Clone or download this repository
gh repo clone treasure-data/treasure-boxes
cd treasure-boxes/engage-box/roi_reporting/agent

# 2. Create project and push agent
tdx llm project create "ROI Reporting Agent"
tdx agent push . -y
```

**That's it!** All components are created:
- ✅ Agent (Dashboard Viz)
- ✅ Knowledge Bases (Database KB + 2 Text KBs)
- ✅ Tools (4 tools)
- ✅ Outputs (3 outputs)
- ✅ Form Interfaces (2 forms)

### Clone to New Project

To create a copy in a different project:

```bash
# 1. Pull existing agent
tdx agent pull "ROI Reporting Agent"

# 2. Create new project
tdx llm project create "My New Project"

# 3. Update project reference
cd agents/ROI\ Reporting\ Agent
echo '{"llm_project": "My New Project"}' > tdx.json

# 4. Push to new project
tdx agent push . -y
```

### Verify Setup

```bash
# Pull back to verify
tdx agent pull "ROI Reporting Agent" -y

# Check created resources
cd agents/ROI\ Reporting\ Agent
ls -la Dashboard\ Viz/agent.yml     # Agent config with tools/outputs
ls -la knowledge_bases/              # Knowledge bases
ls -la form_interfaces/              # Form interfaces
```

## File Structure

```
agent/
├── tdx.json                              # Project reference
├── README.md                             # This file (English)
├── README_JA.md                          # Japanese README
├── Dashboard Viz/
│   ├── prompt.md                         # System prompt (English)
│   ├── prompt_ja.md                      # System prompt (Japanese, reference only)
│   └── agent.yml                         # Agent configuration (includes tools/outputs)
├── knowledge_bases/
│   ├── OverallSummary_Spec.md           # Overall Summary report specification (English)
│   ├── OverallSummary_Spec_ja.md        # Overall Summary report specification (Japanese, reference only)
│   ├── CampaignDetails_Spec.md          # Campaign Details report specification (English)
│   ├── CampaignDetails_Spec_ja.md       # Campaign Details report specification (Japanese, reference only)
│   └── engage_roi_reporting.yml         # Database KB definition
└── form_interfaces/
    ├── Overall Summary.yml               # Form for Overall Summary report
    └── Campaign Details.yml              # Form for Campaign Details report
```

**Note**: Japanese files (`*_ja.md`) are included for reference. The `tdx agent push` command uses English files only. To use Japanese versions, manually replace the files before pushing.

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
| `tdx agent push` fails | Wrong tdx version | Update to tdx 2026.4.55 or later (`npm install -g @treasuredata/tdx`) |

## Revenue Metrics

### Attribution Types
- **Direct Revenue**: Revenue from conversions that occurred within the attribution window after email interaction
- **Contributed Revenue**: Revenue from conversions where email interaction contributed but was not the last touch
- **Total Revenue**: Sum of Direct + Contributed Revenue

### Display Logic
- **Total Revenue** is shown when BOTH direct and contributed revenue exist
- Otherwise, only Direct and/or Contributed Revenue are shown separately

## Advanced: Manual Configuration

If you prefer manual setup via UI or LLM API instead of `tdx agent push`, refer to the [legacy setup documentation](./LEGACY_SETUP.md).

## License

This agent configuration is provided as-is for use with Treasure Data's Engage service.

## Support

For assistance with setup and deployment, consult Treasure Data documentation or your account team.

## Changelog

### 2026-04-13
- **BREAKING**: Updated to tdx CLI format
- Simplified setup to 2 commands (`tdx llm project create` + `tdx agent push`)
- Removed LLM API dependency for setup
- Updated file structure to match `tdx agent pull/push` format
- Form interfaces now use YAML object format instead of JSON strings
- Agent tools and outputs now embedded in `Dashboard Viz/agent.yml`
- Added Japanese files (`*_ja.md`) for reference
