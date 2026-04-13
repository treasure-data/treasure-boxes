# ROIレポーティングエージェント

## 概要

このエージェントは、Treasure DataのEngageサービス向けのROI（投資利益率）レポートを生成します。キャンペーンパフォーマンスデータを自律的に分析し、Trinoに対してSQLクエリを実行し、可視化とインサイトを含むインタラクティブなダッシュボードを生成します。

2種類のレポートをサポートしています:
- **全体サマリーレポート**: 指定期間におけるKPI、トレンド、キャンペーン/ジャーニーのパフォーマンス概要
- **キャンペーン詳細レポート**: 特定のキャンペーンまたはジャーニーの詳細分析（収益アトリビューションを含む）

## 機能

- 自動SQLクエリ生成と実行
- Plotlyによるインタラクティブな可視化
- 多言語サポート（英語/日本語）
- 多通貨サポート（米ドル/円）
- エンゲージメントおよび収益メトリクスのKPIカード
- デュアル軸チャートによる時系列トレンド分析
- 収益アトリビューション付きキャンペーン/ジャーニーパフォーマンステーブル
- コンポーネント失敗時のグレースフルデグラデーション

## ファイル

| ファイル | 説明 |
|---|---|
| `system_prompt.md` | エージェントのシステムプロンプト — System Promptフィールドに貼り付け |
| `knowledge_base_overall_summary.md` | 全体サマリーのレポートスペック — Text KB `OverallSummary_Spec` として登録 |
| `knowledge_base_campaign_details.md` | キャンペーン詳細のレポートスペック — Text KB `CampaignDetails_Spec` として登録 |
| `tools.yml` | 全ツール設定 — エージェントツール設定時の参考資料 |
| `forms/td_managed_overall_summary.yml` | 全体サマリーレポートのフォームインターフェース |
| `forms/td_managed_campaign_details.yml` | キャンペーン詳細レポートのフォームインターフェース |

## 前提条件

### 必要なデータベーステーブル

| テーブル | 説明 | 主要カラム |
|---|---|---|
| `daily_summary` | 日次集計パフォーマンスメトリクス | `summary_date`, `campaign_id`, `journey_id`, `total_sends`, `total_deliveries`, `total_opens`, `total_clicks`, `total_conversions`, `total_revenue_direct`, `total_revenue_contributed` |
| `event_master` | キャンペーン/ジャーニーメタデータ | `campaign_id`, `journey_id`, `campaign_name`, `journey_name` |
| `email_events` | メールイベントログ | `event_timestamp`, `event_type`, `message_id`, `campaign_id`, `journey_id`, `email_title` |
| `revenue` | 収益アトリビューションデータ | `conversion_timestamp`, `conversion_id`, `campaign_id`, `total_revenue`, `attribution_type` |

### データスキーマ要件

**daily_summaryテーブル:**
- `summary_date` (varchar): 'YYYY-MM-DD' 形式の日付
- `campaign_id`, `journey_id` (varchar): 識別子
- `total_sends`, `total_deliveries`, `total_opens`, `total_clicks`, `total_conversions` (integer): イベント数
- `total_hard_bounces`, `total_soft_bounces`, `total_unsubscribes` (integer): ネガティブイベント数
- `total_revenue_direct`, `total_revenue_contributed` (double): 収益額

**email_eventsテーブル:**
- `event_timestamp` (varchar): '%Y-%m-%d %H:%i:%s.%f' 形式のタイムスタンプ
- `event_type` (varchar): 'Send', 'Delivery', 'Open', 'Click', 'Bounce', 'Complaint'
- `message_id` (varchar): 一意のメッセージ識別子
- `email_title` (varchar): メール件名

**revenueテーブル:**
- `conversion_timestamp` (varchar): '%Y-%m-%d %H:%i:%s.%f' 形式のタイムスタンプ
- `attribution_type` (varchar): 'direct' または 'contributed'
- `total_revenue` (double): 収益額

## セットアップ手順

### オプションA: CLI（推奨）

```bash
# 1. このディレクトリをクローンまたはダウンロード
# 2. tools.yml を編集し、<DATABASE_NAME> を実際のデータベース名に置き換え
# 3. 実行:
tdx llm project create "ROI Reporting Agent"
tdx agent push . -f
```

### オプションB: 手動（AI Agent Foundry UI）

#### 1. プロジェクトの作成
AI Agent Foundryで **`ROI Reporting Agent`** という名前の新しいプロジェクトを作成します。

#### 2. データベースをKnowledge Baseとして登録
- タイプ: **Database**
- ROIレポーティングデータベースを選択（daily_summary, email_events, revenueテーブルを含む）

#### 3. レポートスペックをText Knowledge Baseとして登録

**KB 1:**
- タイプ: **Text**, 名前: `OverallSummary_Spec`
- コンテンツ: `knowledge_base_overall_summary.md` から貼り付け

**KB 2:**
- タイプ: **Text**, 名前: `CampaignDetails_Spec`
- コンテンツ: `knowledge_base_campaign_details.md` から貼り付け

#### 4. エージェントの作成
- 名前: **`TD-Managed: Dashboard Viz`**
- System Prompt: `system_prompt.md` から貼り付け
- モデル: Claude 4.5 Sonnet
- Max tool iterations: 4
- Temperature: 0

#### 5. ツールの設定
全ツールの名前、説明、設定については **[tools.yml](./tools.yml)** を参照してください。

#### 6. フォームインターフェースの登録（API利用可能時）
- 全体サマリー: `forms/td_managed_overall_summary.yml`
- キャンペーン詳細: `forms/td_managed_campaign_details.yml`

## 使用方法

### 全体サマリーレポート

```
以下の条件でダッシュボードを作成してください:
- Report_id: 1.Overall Summary
- Start Date: 2025-01-01
- End Date: 2025-01-31
- Timezone: Asia/Tokyo
- Language: Japanese
- Currency: JPY
```

**パラメータ:**
- `Start_date`, `End_date` (必須): 'YYYY-MM-DD' 形式の日付範囲（最大365日）
- `Language` (必須): 'English' または 'Japanese'
- `Currency` (必須): 'USD' または 'JPY'
- `Timezone` (オプション): デフォルトはUTC

### キャンペーン詳細レポート

```
以下の条件でダッシュボードを作成してください:
- Report_id: 2. Campaign Summary
- Campaign_id: ABC123
- Language: Japanese
- Currency: JPY
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

### 全体サマリーには以下が含まれます:
1. エグゼクティブサマリー（データドリブンなインサイト）
2. KPIカード — 送信数、収益、コンバージョン、配信数、開封数、クリック数、バウンス数、配信停止数
3. キャンペーンパフォーマンステーブル（収益上位5件）
4. ジャーニーパフォーマンステーブル（収益上位5件）
5. パフォーマンストレンドチャート（エンゲージメントと収益）
6. データ集計方法に関する注意事項

### キャンペーン詳細には以下が含まれます:
1. エグゼクティブサマリー（データドリブンなインサイト）
2. エンゲージメントKPIカード — 送信数、配信数、開封数、クリック数、バウンス数、配信停止数
3. 収益KPIカード（キャンペーンのみ）— 合計/直接/貢献収益
4. エンゲージメント数トレンドチャート
5. コンバージョン・収益トレンドチャート（キャンペーンのみ）
6. メール件名別パフォーマンステーブル

### 自動粒度
| データ期間 | 粒度 |
|---|---|
| 1–20日 | 日次 |
| 21–89日 | 週次 |
| 90日以上 | 月次 |

## トラブルシューティング

| エラー | 原因 | 対処法 |
|---|---|---|
| "Missing required parameters" | 必須フィルターが未提供 | 全体サマリーには start_date, end_date, language, currency を、キャンペーン詳細には campaign_id または journey_id を指定 |
| "Date range exceeds 365 days" | 日付範囲が長すぎる | 日付範囲を365日以内に縮小 |
| データが返されない | フィルターがデータと一致しない | campaign_id/journey_idが存在することを確認; 日付範囲を確認; テーブル名を確認 |
| スキーマの不一致 | 必須カラムが存在しない | 前提条件に記載されている必須カラムがテーブルに含まれていることを確認 |

## 収益メトリクス

### アトリビューションタイプ
- **直接収益**: メールインタラクション後のアトリビューション期間内に発生したコンバージョンからの収益
- **貢献収益**: メールインタラクションが貢献したが最終タッチではなかったコンバージョンからの収益
- **合計収益**: 直接収益 + 貢献収益の合計

### 表示ロジック
- **合計収益**は、直接収益と貢献収益の両方が存在する場合に表示されます
- それ以外の場合は、直接収益および/または貢献収益が個別に表示されます

## ライセンス
このエージェント設定は、Treasure DataのEngageサービスでの使用を目的として提供されています。

## サポート
これは参考実装です。セットアップとデプロイメントに関する支援については、Treasure Dataのドキュメントまたはアカウントチームにご相談ください。
