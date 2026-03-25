# Email Delivery Reporter Agent

## Overview

This agent generates email delivery reports for Treasure Data's Engage service. It autonomously analyzes email delivery logs from PlazmaDB, executes SQL queries against Trino, and produces interactive dashboards with visualizations and insights.

Two report types are supported:
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

## Files

| File | Description |
|---|---|
| `system_prompt.md` | Agent system prompt — paste into System Prompt field |
| `knowledge_base_overall_summary.md` | Report spec for Overall Summary — register as Text KB named `DeliveryOverallSummary_Spec` |
| `knowledge_base_campaign_summary.md` | Report spec for Campaign Detail — register as Text KB named `DeliveryCampaignSummary_Spec` |
| `tools.yml` | All tool configurations — reference when configuring agent tools |

## Prerequisites

### Required PlazmaDB Database

The database name follows this pattern:
```
delivery_email_<maildomain>
```
Where `<maildomain>` is your email domain with dots replaced by underscores.

**Examples:**
- `example.com` → `delivery_email_example_com`
- `my-company.co.jp` → `delivery_email_my_company_co_jp`

### Required Tables

| Table | Description | Key Columns |
|---|---|---|
| `events` | Email event logs | `time`, `timestamp`, `event_type`, `message_id`, `campaign_id`, `journey_id`, `subject`, `email_sender_id`, `email_template_id` |
| `error_events` | Pre-send failures | `timestamp`, `error_type`, `error_message`, `custom_event_id` |
| `subscription_events` | Opt-out events | `profile_identifier_value`, `campaign_id`, `action`, `received_time`, `time` |

event_type values: `Send`, `Delivery`, `Open`, `Click`, `Bounce`, `Complaint`, `DeliveryDelay`

## Setup Instructions

### Option A: CLI (Recommended)

```bash
# 1. Clone or download this directory
# 2. Edit knowledge_bases/<DB_NAME>.yml with your actual database name
# 3. Run:
tdx llm project create "Email Delivery Reporter"
tdx agent push . -f
```

### Option B: Manual (AI Agent Foundry UI)

#### 1. Create Project
Create a new project named **`Email Delivery Reporter`** in AI Agent Foundry.

#### 2. Register PlazmaDB as Knowledge Base
- Type: **Database**
- Select: `delivery_email_<your_domain>`

#### 3. Register Report Specs as Text Knowledge Bases

**KB 1:**
- Type: **Text**, Name: `DeliveryOverallSummary_Spec`
- Content: paste from `knowledge_base_overall_summary.md`

**KB 2:**
- Type: **Text**, Name: `DeliveryCampaignSummary_Spec`
- Content: paste from `knowledge_base_campaign_summary.md`

#### 4. Create Agent
- Name: **`Email Delivery Reporter`**
- System Prompt: paste from `system_prompt.md`

#### 5. Configure Tools
See **[tools.yml](./tools.yml)** for all tool names, descriptions, and settings.

## Usage

### Overall Summary Report

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

**Parameters:**
- `date_range` (optional): defaults to full data range
- `language` (optional): `'en'` or `'ja'`, defaults to `'en'`
- `campaign_id`, `journey_id`, `subject` (optional): additional filters

### Campaign Detail Report

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

**Parameters:**
- At least one of `campaign_id`, `journey_id`, or `subject` is required
- `date_range`, `language` optional

## Report Components

### Overall Summary includes:
1. Executive Summary
2. KPI Cards — Sends, Deliveries, Unique Opens, Unique Clicks, Bounces, Unsubscribes
3. Performance Trend Chart (dual-axis, auto granularity)
4. Campaign Performance Table (top 100 by sends)
5. Journey Performance Table (top 100 by sends)

### Campaign Detail includes:
1. Executive Summary
2. KPI Cards (filtered)
3. Performance Trend Chart
4. Email Subject Performance Table (top 100 by sends)

### Auto Granularity
| Data span | Granularity |
|---|---|
| 1–34 days | Daily |
| 35–90 days | Weekly |
| 91+ days | Monthly |

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| "No email delivery database found" | DB not registered or wrong name | Verify `delivery_email_<domain>` is registered as KB |
| "Missing required parameters" | Campaign Detail needs at least one identifier | Provide campaign_id, journey_id, or subject |
| No data returned | Filters don't match data | Verify IDs exist; check date range; broaden filters |

## License
This agent configuration is provided as-is for use with Treasure Data's Engage service.

## Support
This is a reference implementation. No support is provided.
