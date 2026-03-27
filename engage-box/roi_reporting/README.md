# ROI Reporting Solution

## Overview

This directory contains a complete ROI (Return on Investment) reporting solution for Treasure Data's Engage service, consisting of two main components:

1. **Data Preparation Workflows** - Automated data collection and aggregation workflows
2. **AI Reporting Agent** - Intelligent dashboard generation agent

## Components

### 1. AI Reporting Agent (`agent/`)

An AI-powered agent that autonomously generates interactive ROI dashboards and reports.

**Features:**
- 📊 Overall Summary Reports - KPIs, trends, and top performers
- 📈 Campaign Detail Reports - Deep-dive analysis with revenue attribution
- 🌐 Multilingual support (English/Japanese)
- 💱 Multi-currency support (USD/JPY)
- 🤖 Autonomous SQL generation and execution
- 📉 Interactive Plotly visualizations

**Quick Start:**
```bash
cd agent/
# See agent/README.md for detailed setup instructions
```

**Documentation:**
- [Agent README (English)](./agent/README.md)
- [Agent README (Japanese)](./agent/README_JA.md)

### 2. Data Preparation Workflows (`workflows/`)

Automated Digdag workflows that prepare data for ROI reporting by:
- Collecting email event data from multiple domains
- Updating Events Master tables from CDP/Engage APIs
- Generating daily summary tables
- Creating revenue attribution data

**Quick Start:**
```bash
cd workflows/reporting_agent/
# See workflows/reporting_agent/README.md for detailed setup instructions
```

**Documentation:**
- [Workflow README](./workflows/reporting_agent/README.md)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ROI Reporting Solution                   │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
         ┌──────────▼─────────┐  ┌─────▼──────────────┐
         │ Data Preparation   │  │  AI Reporting      │
         │    Workflows       │  │     Agent          │
         │  (workflows/)      │  │   (agent/)         │
         └──────────┬─────────┘  └─────┬──────────────┘
                    │                  │
         ┌──────────▼─────────┐        │
         │  Digdag Workflows  │        │
         │  ├─ Events Master  │        │
         │  ├─ Email Events   │        │
         │  ├─ Revenue Data   │        │
         │  └─ Daily Summary  │        │
         └──────────┬─────────┘        │
                    │                  │
         ┌──────────▼──────────────────▼──────────┐
         │        Treasure Data Tables             │
         │  ├─ daily_summary                       │
         │  ├─ email_events                        │
         │  ├─ revenue                             │
         │  └─ event_master                        │
         └─────────────────────────────────────────┘
```

## Getting Started

### Prerequisites

- Treasure Data account with Engage service enabled
- Access to AI Agent Foundry
- Custom Scripts enabled (for workflows)
- Master API key

### Setup Steps

1. **Set up Data Preparation Workflows**
   ```bash
   cd workflows/reporting_agent/
   # Follow instructions in workflows/reporting_agent/README.md
   # This creates the required tables (daily_summary, email_events, revenue, event_master)
   ```

2. **Deploy AI Reporting Agent**
   ```bash
   cd agent/
   # Follow instructions in agent/README.md
   # This sets up the agent in AI Agent Foundry
   ```

3. **Generate Reports**
   - Use the agent via AI Agent Foundry UI
   - Or integrate via Form Interfaces (when API available)

## Required Tables

The solution requires the following tables to be created by the workflow:

| Table | Description | Created By |
|---|---|---|
| `daily_summary` | Daily aggregated performance metrics | Workflow |
| `email_events` | Email event logs (deduplicated) | Workflow |
| `revenue` | Revenue attribution data | Workflow |
| `event_master` | Campaign/journey metadata | Workflow |

## Use Cases

### Overall Summary Report
Get high-level insights across all campaigns and journeys:
- Total sends, deliveries, opens, clicks, conversions
- Revenue breakdown (direct/contributed)
- Top performing campaigns and journeys
- Trend analysis over time

### Campaign Detail Report
Deep-dive into specific campaign or journey performance:
- Unique vs. total engagement metrics
- Email title performance breakdown
- Revenue attribution analysis
- Day-of-week and timing patterns

## Troubleshooting

### Common Issues

| Issue | Solution |
|---|---|
| Agent reports "schema mismatch" | Verify workflow has run successfully and all required tables exist |
| No data in reports | Check workflow execution logs, verify date ranges |
| Form Interfaces not available | API support for Form Interfaces is in development |

### Support Resources

- [Workflow Documentation](./workflows/reporting_agent/README.md)
- [Agent Documentation](./agent/README.md)
- Treasure Data Support Portal

## Development

### Project Structure

```
roi_reporting/
├── README.md                    # This file
├── agent/                       # AI Reporting Agent
│   ├── README.md
│   ├── README_JA.md
│   ├── system_prompt.md
│   ├── system_prompt_JA.md
│   ├── knowledge_base_overall_summary.md
│   ├── knowledge_base_campaign_details.md
│   ├── tools.yml
│   └── forms/
│       ├── td_managed_overall_summary.yml
│       └── td_managed_campaign_details.yml
└── workflows/                   # Data Preparation Workflows
    └── reporting_agent/
        ├── README.md
        ├── config.yaml
        ├── report_preparation.dig
        ├── queries/
        └── scripts/
```

## License

This solution is provided as-is for use with Treasure Data's Engage service.

## Contributing

This is a reference implementation maintained by Treasure Data. For questions or issues, please contact your Treasure Data account team.
