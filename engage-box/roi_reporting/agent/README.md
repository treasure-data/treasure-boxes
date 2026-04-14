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
| `daily_summary` | Daily aggregated performance metrics | `summary_date`, `campaign_id`, `campaign_name`, `journey_id`, `journey_name`, `total_sends`, `total_deliveries`, `total_opens`, `total_clicks`, `total_hard_bounces`, `total_soft_bounces`, `total_unsubscribes`, `total_conversions`, `total_revenue_direct`, `total_revenue_contributed` |
| `events_master` | Campaign/journey metadata | `campaign_id`, `campaign_name`, `journey_id`, `journey_name` |
| `email_events` | Email event logs | `event_timestamp` (ISO8601), `event_type`, `message_id`, `campaign_id`, `journey_id`, `email_title`, `bounce_type` |
| `revenue_table` | Revenue attribution data | `conversion_timestamp` (TIMESTAMP), `conversion_id`, `campaign_id`, `total_revenue`, `attribution_type` |

## Setup Instructions

### Quick Start

```bash
# 1. Clone repository
git clone --depth 1 --filter=blob:none --sparse https://github.com/treasure-data/treasure-boxes.git
cd treasure-boxes
git sparse-checkout set engage-box/roi_reporting
cd engage-box/roi_reporting/agent

# 2. Create database (if not exists)
tdx api -X POST /v3/database/create/engage_roi_reporting
# Note: "Name has already been taken" error is OK if database already exists

# 3. Create LLM project
tdx llm project create "ROI Reporting Agent"

# 4. Push agent
tdx agent push . -f
```

**That's it!** Resources created:
- ✅ Agent: Dashboard Viz
- ✅ Knowledge Bases: 1 Database KB + 2 Text KBs
- ✅ Tools: 4 (list_columns, query_data, Read_OverallSummary_Spec, Read_CampaignDetails_Spec)
- ✅ Outputs: 3 (renderReactApp, text_in_form, new_plot)
- ✅ Form Interfaces: 2

Access your agent:
```bash
# Via CLI
tdx chat "Dashboard Viz"

# Or open in browser: AI Agent Foundry > ROI Reporting Agent > Dashboard Viz
```

### Verify Deployment

```bash
tdx agent show "Dashboard Viz"
```

Expected output:
```
Agent: Dashboard Viz
System Prompt: 6,800+ chars
Tools: 4/4
  - list_columns
  - query_data
  - Read_OverallSummary_Spec
  - Read_CampaignDetails_Spec
Outputs: 3/3
  - renderReactApp
  - text_in_form
  - new_plot
```

### Advanced Options

<details>
<summary>Use a custom project name</summary>

If you want to use a different project name instead of the default "ROI Reporting Agent":

```bash
# 1. Create project with your custom name
tdx llm project create "My Custom ROI Project"

# 2. Update tdx.json
cat > tdx.json << 'EOF'
{
  "llm_project": "My Custom ROI Project",
  "version": "1.0"
}
EOF

# 3. Push agent
tdx agent push . -f
```

**Important**: The project name in `tdx.json` must exactly match your created project name.
</details>

<details>
<summary>Use Japanese Knowledge Bases</summary>

Japanese versions of specifications are available in `docs/japanese/`. The English Knowledge Bases work for both English and Japanese reports by default.

To use Japanese specifications:

```bash
# Replace English files with Japanese versions
cp docs/japanese/OverallSummary_Spec_ja.md knowledge_bases/OverallSummary_Spec.md
cp docs/japanese/CampaignDetails_Spec_ja.md knowledge_bases/CampaignDetails_Spec.md

# Push agent
tdx agent push . -f
```

**Note**: This only affects the specification language. The agent generates Japanese reports when you specify `Language: Japanese` in parameters, regardless of KB language.
</details>

<details>
<summary>Clone to a different project</summary>

To deploy this agent to a different project:

```bash
# 1. Pull existing agent
tdx agent pull "ROI Reporting Agent"

# 2. Create new project
tdx llm project create "My New Project"

# 3. Update project reference
cd agents/ROI\ Reporting\ Agent
echo '{
  "llm_project": "My New Project",
  "version": "1.0"
}' > tdx.json

# 4. Push to new project
tdx agent push . -f
```
</details>

## File Structure

```
agent/
├── README.md                             # This file
├── tdx.json                              # Project reference
├── Dashboard Viz/
│   ├── agent.yml                         # Agent config (tools, outputs, prompt reference)
│   └── prompt.md                         # System prompt (English)
├── knowledge_bases/
│   ├── engage_roi_reporting.yml         # Database KB definition
│   ├── OverallSummary_Spec.md           # Overall Summary specification (English)
│   └── CampaignDetails_Spec.md          # Campaign Details specification (English)
├── form_interfaces/
│   ├── Overall Summary.yml               # Form for Overall Summary report
│   └── Campaign Details.yml              # Form for Campaign Details report
└── docs/
    └── japanese/                         # Japanese reference materials
        ├── OverallSummary_Spec_ja.md    # Overall Summary spec (Japanese)
        ├── CampaignDetails_Spec_ja.md   # Campaign Details spec (Japanese)
        ├── prompt_ja.md                  # System prompt (Japanese)
        └── README_JA.md                  # Japanese README
```

**Notes**:
- Files in `docs/japanese/` are reference materials and are not deployed by default
- `Dashboard Viz/agent.yml` is auto-generated during `tdx agent push` - do not edit directly
- The agent generates reports in both English and Japanese regardless of KB language

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

### Setup Issues

#### "LLM_PROJECT_NOT_FOUND" error

**Cause**: Project name in `tdx.json` doesn't match an existing project  
**Solution**:
```bash
# Check existing projects
tdx llm projects

# Create the project specified in tdx.json
tdx llm project create "ROI Reporting Agent"

# OR update tdx.json to match an existing project
cat > tdx.json << 'EOF'
{
  "llm_project": "Existing Project Name",
  "version": "1.0"
}
EOF
```

#### Database "engage_roi_reporting" not found

**Cause**: Database hasn't been created  
**Solution**:
```bash
tdx api -X POST /v3/database/create/engage_roi_reporting
```

If the database exists but you get this error, verify the name:
```bash
tdx db list | grep engage_roi_reporting
```

#### Tools show 0/4 or outputs missing

**Cause**: Agent configuration wasn't properly loaded during push  
**Solution**:
```bash
# Re-push the agent
tdx agent push . -f

# Verify
tdx agent show "Dashboard Viz"
```

If the issue persists, check that you're in the correct directory (should contain `tdx.json` and `Dashboard Viz/` folder).

#### `tdx agent push` fails

**Cause**: Wrong tdx version  
**Solution**: Update to tdx 2026.4.55 or later:
```bash
tdx upgrade
```

### Usage Issues

#### Agent doesn't generate Japanese reports

**This is not an issue**: The agent generates Japanese reports when you specify `Language: Japanese` in the report parameters. The Knowledge Base language doesn't affect output language.

Example prompt for Japanese report:
```
Create dashboard with following conditions:
- Report_id: 1.Overall Summary
- Start Date: 2025-01-01
- End Date: 2025-01-31
- Language: Japanese
- Currency: JPY
```

#### "Missing required parameters" error

**Cause**: Required filter not provided  
**Solution**: Provide all required parameters:
- Overall Summary: `start_date`, `end_date`, `language`, `currency`
- Campaign Details: `campaign_id` OR `journey_id`, `language`, `currency`

#### "Date range exceeds 365 days" error

**Cause**: Date range too long  
**Solution**: Reduce date range to 365 days or less

#### No data returned

**Cause**: Filters don't match data  
**Solution**:
- Verify campaign_id/journey_id exist in the database
- Check date range matches available data
- Verify table names in Prerequisites

#### Schema mismatch error

**Cause**: Missing required columns  
**Solution**: Verify tables contain required columns as documented in Prerequisites section

### Project Management

#### Need to change project name after deployment

```bash
# 1. Create new project
tdx llm project create "New Project Name"

# 2. Update tdx.json
cat > tdx.json << 'EOF'
{
  "llm_project": "New Project Name",
  "version": "1.0"
}
EOF

# 3. Push to new project (creates new agent instance)
tdx agent push . -f
```

**Note**: This creates a new agent in the new project. The original agent remains in the old project.

### Data Preparation Issues

See the [workflow README](../workflow/README.md) for troubleshooting data preparation and table creation issues.

## Japanese Documentation

Japanese versions of specifications and documentation are available in `docs/japanese/`:

| File | Description |
|------|-------------|
| `OverallSummary_Spec_ja.md` | Overall Summary report specification (Japanese) |
| `CampaignDetails_Spec_ja.md` | Campaign Details report specification (Japanese) |
| `prompt_ja.md` | System prompt reference (Japanese) |
| `README_JA.md` | Japanese README |

**Note**: These are reference materials. The English specifications are sufficient for all functionality, including Japanese report generation. The agent can generate reports in Japanese when you specify `Language: Japanese` in the report parameters.

To deploy Japanese specifications instead of English (advanced):
```bash
cp docs/japanese/OverallSummary_Spec_ja.md knowledge_bases/OverallSummary_Spec.md
cp docs/japanese/CampaignDetails_Spec_ja.md knowledge_bases/CampaignDetails_Spec.md
tdx agent push . -f
```

## Revenue Metrics

### Attribution Types
- **Direct Revenue**: Revenue from conversions that occurred within the attribution window after email interaction
- **Contributed Revenue**: Revenue from conversions where email interaction contributed but was not the last touch
- **Total Revenue**: Sum of Direct + Contributed Revenue

### Display Logic
- **Total Revenue** is shown when BOTH direct and contributed revenue exist
- Otherwise, only Direct and/or Contributed Revenue are shown separately

## Advanced: Manual Configuration via UI

If you prefer to set up via the Agent Foundry UI instead of `tdx agent push`, follow these steps using the files in this repository as reference:

### 1. Create Project

Navigate to Agent Foundry in the TD Console and create a new project named "ROI Reporting Agent".

### 2. Create Knowledge Bases

**Database KB:**
- Type: Database
- Name: `engage_roi_reporting`
- Database: `engage_roi_reporting`
- Reference: `knowledge_bases/engage_roi_reporting.yml`

**Text KBs** (create two):
- Type: Text
- Name: `OverallSummary_Spec` — copy content from `knowledge_bases/OverallSummary_Spec.md`
- Name: `CampaignDetails_Spec` — copy content from `knowledge_bases/CampaignDetails_Spec.md`

### 3. Create Agent

- Name: `Dashboard Viz`
- Model: `claude-4.5-sonnet`
- Temperature: `0`
- Max Tool Iterations: `4`
- System Prompt: copy content from `Dashboard Viz/prompt.md`
- Tools and Outputs: configure as defined in `Dashboard Viz/agent.yml`

### 4. Create Form Interfaces

Create two form interfaces using the definitions in:
- `form_interfaces/Overall Summary.yml`
- `form_interfaces/Campaign Details.yml`

Each file contains `form_schema` (JSON Schema) and `ui_schema` (UI rendering hints) to copy into the respective UI fields.

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
