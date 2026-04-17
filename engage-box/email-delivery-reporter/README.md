# Email Delivery Reporter

An AI agent that automatically analyzes Treasure Data Engage email delivery logs from PlazmaDB and generates interactive React + Plotly dashboards. Supports English and Japanese, USD and JPY.

## Overview

This agent generates email delivery reports for Treasure Data's Engage service. It autonomously analyzes email delivery logs from PlazmaDB, executes SQL queries against Trino, and produces interactive dashboards with visualizations and insights.

Two report types are supported:
- **Overall Summary Report**: High-level KPIs, trends, and campaign/journey performance over a period
- **Campaign Detail Report**: Detailed analysis for a specific campaign, journey, or subject filter

## Features

- Automated SQL query generation and execution
- Interactive visualizations with Plotly
- Multilingual support (English/Japanese)
- Multi-currency support (USD/JPY)
- KPI cards with engagement and quality metrics
- Time-series trend analysis with dual-axis charts
- Campaigns/journeys/subjects performance tables
- Graceful degradation when components fail

## Repository Structure

```
email-delivery-reporter/
├── tdx.json                                    # Project manifest (no changes needed)
├── README.md                                   # This file
├── Email Delivery Dashboard/
│   ├── agent.yml                               # ← EDIT: replace DOMAIN (2 places)
│   └── prompt.md                               # System prompt (no changes needed)
├── knowledge_bases/
│   ├── delivery_email_DOMAIN.yml               # ← EDIT: replace DOMAIN (filename + 2 places inside)
│   ├── OverallSummary_Spec.md                  # Report spec (no changes needed)
│   └── CampaignSummary_Spec.md                 # Report spec (no changes needed)
├── form_interfaces/
│   ├── Overall Summary.yml                     # Form UI (no changes needed)
│   └── Campaign Details.yml                    # Form UI (no changes needed)
└── docs/japanese/                              # Japanese documentation (reference only, not deployed)
```

## Prerequisites

- `tdx` CLI (v2026.4.55+), authenticated (`tdx auth setup`)
- Treasure Data account with Engage enabled
- PlazmaDB database `delivery_email_<domain>` must exist

### Required PlazmaDB Database

The database name follows this pattern:
```
delivery_email_<maildomain>
```
Where `<maildomain>` is your email domain with dots and hyphens replaced by underscores.

**Examples:**
- `example.com` → `delivery_email_example_com`
- `my-company.co.jp` → `delivery_email_my_company_co_jp`

### Required Tables

| Table | Description | Key Columns |
|---|---|---|
| `events` | Email event logs | `time`, `timestamp`, `event_type`, `message_id`, `campaign_id`, `journey_id`, `subject`, `email_sender_id`, `email_template_id` |
| `error_events` | Pre-send failures | `timestamp`, `error_type`, `error_message`, `custom_event_id` |
| `subscription_events` | Opt-out events | `profile_identifier_value`, `campaign_id`, `action`, `received_time`, `time` |

Event types: `Send`, `Delivery`, `Open`, `Click`, `Bounce`, `Complaint`, `DeliveryDelay`

## Quick Start

### Step 1: Clone

```bash
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/treasure-data/treasure-boxes.git
cd treasure-boxes
git sparse-checkout set engage-box/email-delivery-reporter
cd engage-box/email-delivery-reporter
```

### Step 2: Determine your domain slug

Derive the database name from your Engage sending email domain:
- Replace dots and hyphens with underscores
- Example: `example.com` → `example_com`, `my-company.co.jp` → `my_company_co_jp`

Verify the database exists:

```bash
tdx databases | grep delivery_email
```

### Step 3: Replace DOMAIN (5 replacements across 2 files + 1 rename)

The following example uses `example_com`. Replace with your actual domain slug.

| # | File | Location | Before → After |
|---|------|----------|----------------|
| 1 | `knowledge_bases/delivery_email_DOMAIN.yml` | **Filename** | → `delivery_email_example_com.yml` |
| 2 | Same file | `name:` (line 1) | `delivery_email_DOMAIN` → `delivery_email_example_com` |
| 3 | Same file | `database:` (line 3) | `delivery_email_DOMAIN` → `delivery_email_example_com` |
| 4 | `Email Delivery Dashboard/agent.yml` | 1st `@ref` | `"delivery_email_DOMAIN"` → `"delivery_email_example_com"` |
| 5 | Same file | 2nd `@ref` | `"delivery_email_DOMAIN"` → `"delivery_email_example_com"` |

Commands (replace `example_com` with your slug):

```bash
# Rename the knowledge base file
mv knowledge_bases/delivery_email_DOMAIN.yml \
   knowledge_bases/delivery_email_example_com.yml

# Update file contents (both files at once)
# macOS / BSD:
sed -i '' 's/delivery_email_DOMAIN/delivery_email_example_com/g' \
  knowledge_bases/delivery_email_example_com.yml \
  "Email Delivery Dashboard/agent.yml"

# Linux (GNU sed):
sed -i 's/delivery_email_DOMAIN/delivery_email_example_com/g' \
  knowledge_bases/delivery_email_example_com.yml \
  "Email Delivery Dashboard/agent.yml"
```

### Step 4: Deploy

```bash
tdx llm project create "Email Delivery Reporter"
tdx agent push . -f
```

Expected output:
```
Push summary for 'Email Delivery Reporter':
  + 6 new
  Agents: 1 created
  Knowledge Bases: 1 created
  Text Knowledge Bases: 2 created
  Form Interfaces: 2 created

✔ Pushed 6 resources to 'Email Delivery Reporter'
```

### Step 5: Verify

```bash
tdx agent list
```

Or open: AI Agent Foundry > Email Delivery Reporter > Email Delivery Dashboard

## Usage

### Overall Summary Report

**Example (English):**
```
Generate an overall email delivery report with following conditions:
- Report_id: 1. Overall Summary
- Start Date: 2025-01-01
- End Date: 2025-01-31
- Language: English
- Currency: USD
```

**Example (Japanese):**
```
以下の条件でメール配信の全体サマリーレポートを作成してください:
- Report_id: 1. Overall Summary
- Start Date: 2025-01-01
- End Date: 2025-01-31
- Language: Japanese
- Currency: JPY
```

**Parameters:** 
- `Start_date`, `End_date` (required, max 365 days apart)
- `Language` (`English` or `Japanese`)
- `Currency` (`USD` or `JPY`)

### Campaign Detail Report

**Example (English):**
```
Generate a detailed email delivery report with following conditions:
- Report_id: 2. Campaign Summary
- Campaign_id: ABC123
- Language: English
- Currency: USD
```

**Example (Japanese):**
```
以下の条件でキャンペーン詳細レポートを作成してください:
- Report_id: 2. Campaign Summary
- Campaign_id: ABC123
- Language: Japanese
- Currency: JPY
```

**Parameters:**
- `Campaign_id` or `Journey_id` (at least one required)
- `Language` (`English` or `Japanese`)
- `Currency` (`USD` or `JPY`)
- Optional: `date_range`, `subject` filter

## Report Components

### Overall Summary includes:
1. Executive Summary
2. KPI Cards — Sends, Deliveries, Unique Opens, Unique Clicks, Bounces, Unsubscribes
3. Performance Trend Chart (dual-axis, auto granularity)
4. Campaign Performance Table (top 100 by sends)
5. Journey Performance Table (top 100 by sends)

### Campaign Detail includes:
1. Executive Summary
2. KPI Cards (filtered by campaign/journey)
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
| Knowledge base not found | `name` in `.yml` doesn't match `@ref` in `agent.yml` | Check all 5 DOMAIN replacements above |
| Database not found | `database:` field doesn't match existing TD database | Run `tdx databases \| grep delivery_email` to verify |
| `tdx agent push` structure error | `knowledge_bases/` not at project root | Ensure `knowledge_bases/` is at same level as `tdx.json`, not nested in `agent/` |
| LLM_PROJECT_NOT_FOUND | Project not created | Run `tdx llm project create "Email Delivery Reporter"` first |
| No data returned | Filter doesn't match data or date range too narrow | Verify campaign_id/journey_id exists; widen date range; check filters |
| "Missing required parameters" | Campaign Detail needs at least one identifier | Provide campaign_id or journey_id |

## License
This agent configuration is provided as-is for use with Treasure Data's Engage service.

## Support
For questions or issues, please contact your Treasure Data support team.
