# Email Delivery Reporter Agent

## 概要

このエージェントは、Treasure Data の Engage サービス向けにメール配信レポートを生成します。PlazmaDB のメール配信ログを自動的に分析し、Trino に対して SQL クエリを実行し、ビジュアライゼーションとインサイトを含むインタラクティブなダッシュボードを生成します。

2種類のレポートをサポートします：
- **全体サマリーレポート**: 期間全体の高レベル KPI、トレンド、キャンペーン/ジャーニーのパフォーマンス
- **キャンペーン詳細レポート**: 特定のキャンペーンまたはジャーニーの詳細分析

## 機能

- SQL クエリの自動生成と実行
- インタラクティブなビジュアライゼーション
- 多言語サポート（英語/日本語）
- 多通貨サポート（USD/JPY）
- エンゲージメントと品質メトリクスを含む KPI カード
- 時系列トレンド分析
- キャンペーン/ジャーニーのパフォーマンステーブル
- コンポーネント失敗時の優雅な劣化

## ファイル構成

```
email-delivery-reporter/
├── tdx.json                                    # プロジェクトマニフェスト（変更不要）
├── Email Delivery Dashboard/
│   ├── agent.yml                               # ← 編集: DOMAIN を置換（2箇所）
│   └── prompt.md                               # システムプロンプト（変更不要）
├── knowledge_bases/
│   ├── delivery_email_DOMAIN.yml               # ← 編集: DOMAIN を置換（ファイル名 + 内容2箇所）
│   ├── OverallSummary_Spec.md                  # レポート仕様（変更不要）
│   └── CampaignSummary_Spec.md                 # レポート仕様（変更不要）
├── form_interfaces/
│   ├── Overall Summary.yml                     # フォーム UI（変更不要）
│   └── Campaign Details.yml                    # フォーム UI（変更不要）
└── docs/japanese/                              # 参考資料のみ（デプロイ対象外）
```

## 前提条件

- `tdx` CLI (v2026.4.55+)、認証済み (`tdx auth setup`)
- Engage が有効な Treasure Data アカウント
- PlazmaDB データベース `delivery_email_<ドメイン>` が存在すること

## セットアップ手順

### ステップ 1: クローン

```bash
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/treasure-data/treasure-boxes.git
cd treasure-boxes
git sparse-checkout set engage-box/email-delivery-reporter
cd engage-box/email-delivery-reporter
```

### ステップ 2: ドメインスラッグの特定

Engage の送信元メールドメインからデータベース名を導出します：
- ドットとハイフンをアンダースコアに置換
- 例: `example.com` → `example_com`, `my-company.co.jp` → `my_company_co_jp`

データベースが存在するか確認：

```bash
tdx databases | grep delivery_email
```

### ステップ 3: DOMAIN の置換（2ファイル + 1リネーム、計5箇所）

以下の例では `example_com` を使用しています。ご自身のドメインスラッグに置き換えてください。

| # | ファイル | 場所 | 変更前 → 変更後 |
|---|---------|------|----------------|
| 1 | `knowledge_bases/delivery_email_DOMAIN.yml` | **ファイル名** | → `delivery_email_example_com.yml` |
| 2 | 同上 | `name:` (1行目) | `delivery_email_DOMAIN` → `delivery_email_example_com` |
| 3 | 同上 | `database:` (3行目) | `delivery_email_DOMAIN` → `delivery_email_example_com` |
| 4 | `Email Delivery Dashboard/agent.yml` | 1つ目の `@ref` | `"delivery_email_DOMAIN"` → `"delivery_email_example_com"` |
| 5 | 同上 | 2つ目の `@ref` | `"delivery_email_DOMAIN"` → `"delivery_email_example_com"` |

コマンド（`example_com` をご自身のスラッグに置き換えてください）：

```bash
# ナレッジベースファイルのリネーム
mv knowledge_bases/delivery_email_DOMAIN.yml \
   knowledge_bases/delivery_email_example_com.yml

# ファイル内容の一括置換
# macOS / BSD:
sed -i '' 's/delivery_email_DOMAIN/delivery_email_example_com/g' \
  knowledge_bases/delivery_email_example_com.yml \
  "Email Delivery Dashboard/agent.yml"

# Linux (GNU sed):
sed -i 's/delivery_email_DOMAIN/delivery_email_example_com/g' \
  knowledge_bases/delivery_email_example_com.yml \
  "Email Delivery Dashboard/agent.yml"
```

### ステップ 4: デプロイ

```bash
tdx llm project create "Email Delivery Reporter"
tdx agent push . -f
```

### ステップ 5: 確認

```bash
tdx agent list
```

または: AI Agent Foundry > Email Delivery Reporter > Email Delivery Dashboard

## 使用方法

### 全体サマリーレポート

```
Generate an overall email delivery report with following conditions:
- Report_id: 1. Overall Summary
- Start Date: 2025-01-01
- End Date: 2025-01-31
- Language: English
- Currency: USD
```

```
以下の条件でメール配信レポートを作成してください：
- Report_id: 1. Overall Summary
- Start Date: 2024-12-01
- End Date: 2024-12-31
- Language: Japanese
- Currency: JPY
```

パラメータ: `Start_date`, `End_date`（必須、最大365日）、`Language`（`English`/`Japanese`）、`Currency`（`USD`/`JPY`）

### キャンペーン詳細レポート

```
Generate a detailed email delivery report with following conditions:
- Report_id: 2. Campaign Summary
- Campaign_id: ABC123
- Language: English
- Currency: USD
```

パラメータ: `Campaign_id` または `Journey_id`（いずれか必須）、`Language`、`Currency`

## トラブルシューティング

| エラー | 原因 | 解決策 |
|---|---|---|
| Knowledge base not found | `.yml` の `name` が `agent.yml` の `@ref` と不一致 | 上記5箇所の DOMAIN 置換を確認 |
| Database not found | `database:` フィールドが既存の TD データベースと不一致 | `tdx databases \| grep delivery_email` で確認 |
| `tdx agent push` 構造エラー | `knowledge_bases/` がプロジェクトルートにない | `knowledge_bases/` が `tdx.json` と同じ階層にあることを確認 |
| LLM_PROJECT_NOT_FOUND | プロジェクト未作成 | `tdx llm project create "Email Delivery Reporter"` を先に実行 |
| データが返されない | フィルタがデータにマッチしない | campaign_id/journey_id の存在確認、日付範囲の拡大 |
