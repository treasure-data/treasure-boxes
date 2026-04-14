# ROI レポート エージェント

## 概要

このエージェントは、Treasure DataのEngageサービス向けにROI（投資収益率）レポートを生成します。キャンペーンパフォーマンスデータを自律的に分析し、Trinoに対してSQLクエリを実行し、可視化とインサイトを含むインタラクティブなダッシュボードを生成します。

2種類のレポートタイプをサポート:
- **Overall Summaryレポート**: 指定期間における高レベルKPI、トレンド、キャンペーン/ジャーニーパフォーマンス
- **Campaign Detailレポート**: 特定のキャンペーンまたはジャーニーの詳細分析（収益アトリビューションを含む）

## 機能

- 自動SQLクエリ生成・実行
- Plotlyによるインタラクティブな可視化
- 多言語サポート（英語/日本語）
- 多通貨サポート（USD/JPY）
- エンゲージメントと収益メトリクスのKPIカード
- デュアル軸チャートによる時系列トレンド分析
- 収益アトリビューション付きキャンペーン/ジャーニーパフォーマンステーブル
- コンポーネント障害時のグレースフルデグラデーション

## 前提条件

### 必要なツール

- `tdx` CLI (バージョン 2026.4.55 以降)
- Git または `gh` CLI（リポジトリクローン用）

### データ準備

このエージェントを使用する前に、必要なデータベーステーブルを準備する必要があります。treasure-boxesリポジトリの`roi_reporting`ワークフローが、これらのテーブルを作成するためのリファレンス実装を提供しています。

### 必要なデータベーステーブル

エージェントは`engage_roi_reporting`データベースに以下のテーブルを必要とします:

| テーブル | 説明 | 主要カラム |
|---|---|---|
| `daily_summary` | 日次集計パフォーマンスメトリクス | `summary_date`, `campaign_id`, `campaign_name`, `journey_id`, `journey_name`, `total_sends`, `total_deliveries`, `total_opens`, `total_clicks`, `total_hard_bounces`, `total_soft_bounces`, `total_unsubscribes`, `total_conversions`, `total_revenue_direct`, `total_revenue_contributed` |
| `events_master` | キャンペーン/ジャーニーメタデータ | `campaign_id`, `campaign_name`, `journey_id`, `journey_name` |
| `email_events` | メールイベントログ | `event_timestamp` (ISO8601), `event_type`, `message_id`, `campaign_id`, `journey_id`, `email_title`, `bounce_type` |
| `revenue_table` | 収益アトリビューションデータ | `conversion_timestamp` (TIMESTAMP), `conversion_id`, `campaign_id`, `total_revenue`, `attribution_type` |

## セットアップ手順

### クイックスタート

```bash
# 1. このリポジトリをクローンまたはダウンロード
gh repo clone treasure-data/treasure-boxes
cd treasure-boxes/engage-box/roi_reporting/agent

# 2. プロジェクトを作成してエージェントをプッシュ
tdx llm project create "ROI Reporting Agent"
tdx agent push . -f
```

**これだけです！** すべてのコンポーネントが作成されます:
- ✅ エージェント (Dashboard Viz)
- ✅ ナレッジベース (Database KB + 2つのText KB)
- ✅ ツール (4つ)
- ✅ 出力 (3つ)
- ✅ フォームインターフェース (2つ)

### 新しいプロジェクトへのクローン

別のプロジェクトにコピーを作成する場合:

```bash
# 1. 既存のエージェントをプル
tdx agent pull "ROI Reporting Agent"

# 2. 新しいプロジェクトを作成
tdx llm project create "My New Project"

# 3. プロジェクト参照を更新
cd agents/ROI\ Reporting\ Agent
echo '{"llm_project": "My New Project"}' > tdx.json

# 4. 新しいプロジェクトにプッシュ
tdx agent push . -f
```

### セットアップの確認

```bash
# プルバックして確認
tdx agent pull "ROI Reporting Agent" -y

# 作成されたリソースを確認
cd agents/ROI\ Reporting\ Agent
ls -la Dashboard\ Viz/agent.yml     # ツール/出力を含むエージェント設定
ls -la knowledge_bases/              # ナレッジベース
ls -la form_interfaces/              # フォームインターフェース
```

## ファイル構成

```
agent/
├── tdx.json                              # プロジェクト参照
├── README.md                             # 英語版README
├── README_JA.md                          # このファイル（日本語版README）
├── Dashboard Viz/
│   ├── prompt.md                         # システムプロンプト（英語）
│   ├── prompt_ja.md                      # システムプロンプト（日本語）
│   └── agent.yml                         # エージェント設定（ツール/出力を含む）
├── knowledge_bases/
│   ├── OverallSummary_Spec.md           # Overall Summaryレポート仕様（英語）
│   ├── OverallSummary_Spec_ja.md        # Overall Summaryレポート仕様（日本語）
│   ├── CampaignDetails_Spec.md          # Campaign Detailsレポート仕様（英語）
│   ├── CampaignDetails_Spec_ja.md       # Campaign Detailsレポート仕様（日本語）
│   └── engage_roi_reporting.yml         # Database KB定義
└── form_interfaces/
    ├── Overall Summary.yml               # Overall Summaryレポート用フォーム
    └── Campaign Details.yml              # Campaign Detailsレポート用フォーム
```

**注意**: 日本語版ファイル（`*_ja.md`）は参照用に含まれていますが、`tdx agent push`では英語版ファイルのみが使用されます。日本語版を使用したい場合は、手動でファイルを置き換えてください。

## 使い方

### Overall Summaryレポート

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

**パラメータ:**
- `Start_date`, `End_date` (必須): 'YYYY-MM-DD'形式の日付範囲（最大365日）
- `Language` (必須): 'English' または 'Japanese'
- `Currency` (必須): 'USD' または 'JPY'
- `Timezone` (オプション): デフォルトはUTC

### Campaign Detailレポート

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

**パラメータ:**
- `Campaign_id` または `Journey_id` (いずれか必須): キャンペーンまたはジャーニーの識別子
- `Language` (必須): 'English' または 'Japanese'
- `Currency` (必須): 'USD' または 'JPY'

## レポートコンポーネント

### Overall Summaryレポートに含まれるもの:
1. エグゼクティブサマリー（データドリブンなインサイト）
2. KPIカード — Sends, Revenue, Conversions, Deliveries, Opens, Clicks, Bounces, Unsubscribes
3. キャンペーンパフォーマンステーブル（収益上位5件）
4. ジャーニーパフォーマンステーブル（収益上位5件）
5. パフォーマンストレンドチャート（エンゲージメントと収益）
6. データ手法に関する免責事項

### Campaign Detailレポートに含まれるもの:
1. エグゼクティブサマリー（データドリブンなインサイト）
2. エンゲージメントKPIカード — Sends, Deliveries, Opens, Clicks, Bounces, Unsubscribes
3. 収益KPIカード（キャンペーンのみ）— Total/Direct/Contributed Revenue
4. エンゲージメント数トレンドチャート
5. コンバージョン＆収益トレンドチャート（キャンペーンのみ）
6. メールタイトル別パフォーマンステーブル

### 自動粒度調整
| データ期間 | 粒度 |
|---|---|
| 1～20日 | 日次 |
| 21～89日 | 週次 |
| 90日以上 | 月次 |

## トラブルシューティング

| エラー | 原因 | 解決方法 |
|---|---|---|
| "Missing required parameters" | 必須パラメータが不足 | Overall Summaryでは start_date, end_date, language, currency を指定。Campaign Detailsでは campaign_id または journey_id を指定 |
| "Date range exceeds 365 days" | 日付範囲が長すぎる | 日付範囲を365日以内に縮小 |
| データが返されない | フィルターがデータと一致しない | campaign_id/journey_id の存在確認、日付範囲確認、テーブル名確認 |
| スキーマの不一致 | 必須カラムが不足 | 前提条件セクションに記載された必須カラムがテーブルに含まれているか確認 |
| `tdx agent push` が失敗 | tdxバージョンが古い | tdx 2026.4.55以降に更新 (`npm install -g @treasuredata/tdx`) |

## 収益メトリクス

### アトリビューションタイプ
- **Direct Revenue**: メールインタラクション後のアトリビューションウィンドウ内で発生したコンバージョンからの収益
- **Contributed Revenue**: メールインタラクションが貢献したものの最終タッチではなかったコンバージョンからの収益
- **Total Revenue**: Direct + Contributed Revenueの合計

### 表示ロジック
- **Total Revenue**は、DirectとContributed Revenueの両方が存在する場合に表示
- それ以外の場合は、DirectまたはContributed Revenueのみが個別に表示

## 上級: UIによる手動設定

`tdx agent push` の代わりに Agent Foundry UIでセットアップしたい場合は、このリポジトリのファイルをリファレンスとして以下の手順に従ってください:

### 1. プロジェクト作成

TD ConsoleのAgent Foundryで「ROI Reporting Agent」という名前の新しいプロジェクトを作成します。

### 2. ナレッジベースの作成

**Database KB:**
- タイプ: Database
- 名前: `engage_roi_reporting`
- データベース: `engage_roi_reporting`
- リファレンス: `knowledge_bases/engage_roi_reporting.yml`

**Text KB** (2つ作成):
- タイプ: Text
- 名前: `OverallSummary_Spec` — `knowledge_bases/OverallSummary_Spec.md` の内容をコピー
- 名前: `CampaignDetails_Spec` — `knowledge_bases/CampaignDetails_Spec.md` の内容をコピー

### 3. エージェントの作成

- 名前: `Dashboard Viz`
- モデル: `claude-4.5-sonnet`
- Temperature: `0`
- Max Tool Iterations: `4`
- システムプロンプト: `Dashboard Viz/prompt.md` の内容をコピー
- ツールと出力: `Dashboard Viz/agent.yml` に定義された内容を設定

### 4. フォームインターフェースの作成

以下の定義ファイルを使用してフォームインターフェースを2つ作成:
- `form_interfaces/Overall Summary.yml`
- `form_interfaces/Campaign Details.yml`

各ファイルには `form_schema`（JSON Schema）と `ui_schema`（UI表示ヒント）が含まれているので、それぞれUIのフィールドにコピーしてください。

## ライセンス

このエージェント設定は、Treasure DataのEngageサービスで使用するためのものとして提供されています。

## サポート

セットアップとデプロイに関するサポートについては、Treasure Dataのドキュメントまたは担当アカウントチームにお問い合わせください。

## 変更履歴

### 2026-04-13
- **BREAKING**: tdx CLI形式に更新
- セットアップを2コマンドに簡素化 (`tdx llm project create` + `tdx agent push`)
- セットアップ時のLLM API依存性を削除
- ファイル構成を`tdx agent pull/push`形式に合わせて更新
- フォームインターフェースがJSON文字列形式からYAMLオブジェクト形式に変更
- エージェントのツールと出力を`Dashboard Viz/agent.yml`に統合
- 日本語版ファイル（`*_ja.md`）を参照用に追加
