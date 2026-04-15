# Email Delivery Reporter

Treasure Data Engage のメール配信ログ (PlazmaDB) を自動分析し、React + Plotly のインタラクティブダッシュボードを生成する AI エージェントです。英語・日本語、USD・JPY に対応しています。

## Repository Structure

```
email-delivery-reporter/
├── tdx.json                                    # Project manifest (no changes needed)
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
└── docs/japanese/                              # Reference only (not deployed)
```

## Prerequisites

- `tdx` CLI (v2026.4.55+), authenticated (`tdx auth setup`)
- Treasure Data account with Engage enabled
- PlazmaDB database `delivery_email_<domain>` が存在すること

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

Engage の送信元メールドメインからデータベース名を導出します:
- ドットとハイフンをアンダースコアに置換
- 例: `example.com` → `example_com`, `my-company.co.jp` → `my_company_co_jp`

データベースが存在するか確認:

```bash
tdx databases | grep delivery_email
```

### Step 3: Replace DOMAIN (5 replacements across 2 files + 1 rename)

以下の例では `example_com` を使用しています。ご自身のドメインスラッグに置き換えてください。

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

```
Generate an overall email delivery report with following conditions:
- Report_id: 1. Overall Summary
- Start Date: 2025-01-01
- End Date: 2025-01-31
- Language: English
- Currency: USD
```

Parameters: `Start_date`, `End_date` (required, max 365 days), `Language` (`English`/`Japanese`), `Currency` (`USD`/`JPY`)

### Campaign Detail Report

```
Generate a detailed email delivery report with following conditions:
- Report_id: 2. Campaign Summary
- Campaign_id: ABC123
- Language: English
- Currency: USD
```

Parameters: `Campaign_id` or `Journey_id` (one required), `Language`, `Currency`

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| Knowledge base not found | `name` in `.yml` doesn't match `@ref` in `agent.yml` | Check all 5 DOMAIN replacements above |
| Database not found | `database:` field doesn't match existing TD database | Run `tdx databases \| grep delivery_email` |
| `tdx agent push` structure error | `knowledge_bases/` not at project root | Ensure `knowledge_bases/` is at same level as `tdx.json`, not nested in `agent/` |
| LLM_PROJECT_NOT_FOUND | Project not created | Run `tdx llm project create "Email Delivery Reporter"` first |
| No data returned | Filter doesn't match data | Verify campaign_id/journey_id exists, widen date range |
