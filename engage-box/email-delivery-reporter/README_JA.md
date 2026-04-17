# Email Delivery Reporter Agent

## 概要

このエージェントは、Treasure Data の Engage サービス向けにメール配信レポートを生成します。PlazmaDB のメール配信ログを自動的に分析し、Trino に対して SQL クエリを実行し、ビジュアライゼーションとインサイトを含むインタラクティブなダッシュボードを生成します。

2種類のレポートをサポートします：
- **全体サマリーレポート**: 期間全体の高レベル KPI、トレンド、キャンペーン/ジャーニーのパフォーマンス
- **キャンペーン詳細レポート**: 特定のキャンペーン、ジャーニー、または件名フィルタの詳細分析

## 機能

- SQL クエリの自動生成と実行
- インタラクティブなビジュアライゼーション
- 多言語サポート（英語/日本語）
- エンゲージメントと品質メトリクスを含む KPI カード
- デュアル軸チャートによる時系列トレンド分析
- キャンペーン/ジャーニー/件名のパフォーマンステーブル
- コンポーネント失敗時の優雅な劣化

## ファイル構成

| ファイル | 説明 |
|---|---|
| `system_prompt.md` | エージェントのシステムプロンプト（英語・正式版）|
| `system_prompt_JA.md` | システムプロンプトの日本語参考訳 |
| `knowledge_base_overall_summary.md` | Overall Summary レポート仕様（英語・正式版）— `DeliveryOverallSummary_Spec` として登録 |
| `knowledge_base_campaign_summary.md` | Campaign Detail レポート仕様（英語・正式版）— `DeliveryCampaignSummary_Spec` として登録 |
| `knowledge_base_overall_summary_JA.md` | Overall Summary レポート仕様の日本語参考訳 |
| `knowledge_base_campaign_summary_JA.md` | Campaign Detail レポート仕様の日本語参考訳 |
| `tools.yml` | ツール設定（エージェントツール設定時に参照）|

## 前提条件

### 必要な PlazmaDB データベース

データベース名は以下のパターンに従います：
```
delivery_email_<メールドメイン>
```
ドットをアンダースコアに置き換えます。

**例:**
- `example.com` → `delivery_email_example_com`
- `my-company.co.jp` → `delivery_email_my_company_co_jp`

### 必要なテーブル

| テーブル | 説明 | 主要カラム |
|---|---|---|
| `events` | メールイベントログ | `time`, `timestamp`, `event_type`, `message_id`, `campaign_id`, `journey_id`, `subject`, `email_sender_id`, `email_template_id` |
| `error_events` | 送信前の失敗 | `timestamp`, `error_type`, `error_message`, `custom_event_id` |
| `subscription_events` | オプトアウトイベント | `profile_identifier_value`, `campaign_id`, `action`, `received_time`, `time` |

event_type の値: `Send`, `Delivery`, `Open`, `Click`, `Bounce`, `Complaint`, `DeliveryDelay`

## セットアップ手順

### オプション A: CLI（推奨）

```bash
# 1. このディレクトリをクローンまたはダウンロード
# 2. knowledge_bases/<DB_NAME>.yml を実際のデータベース名で編集
# 3. 実行:
tdx llm project create "Email Delivery Reporter"
tdx agent push . -f
```

### オプション B: 手動（AI Agent Foundry UI）

#### 1. プロジェクト作成
AI Agent Foundry で **`Email Delivery Reporter`** という名前のプロジェクトを作成します。

#### 2. PlazmaDB をナレッジベースとして登録
- タイプ: **Database**
- 選択: `delivery_email_<あなたのドメイン>`

#### 3. レポート仕様をテキストナレッジベースとして登録

**KB 1:**
- タイプ: **Text**、名前: `DeliveryOverallSummary_Spec`
- コンテンツ: `knowledge_base_overall_summary.md` から貼り付け

**KB 2:**
- タイプ: **Text**、名前: `DeliveryCampaignSummary_Spec`
- コンテンツ: `knowledge_base_campaign_summary.md` から貼り付け

#### 4. エージェント作成
- 名前: **`Email Delivery Reporter`**
- システムプロンプト: `system_prompt.md` から貼り付け

#### 5. ツール設定
**[tools.yml](./tools.yml)** を参照してすべてのツール設定を行います。

## 使用方法

### 全体サマリーレポート

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

**パラメータ:**
- `date_range`（オプション）: 省略時は全データ範囲
- `language`（オプション）: `'en'` または `'ja'`、デフォルトは `'en'`
- `campaign_id`, `journey_id`, `subject`（オプション）: 追加フィルタ

### キャンペーン詳細レポート

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

**パラメータ:**
- `campaign_id`、`journey_id`、`subject` のいずれか1つ以上が必須
- `date_range`、`language` はオプション

## レポートコンポーネント

### 全体サマリーに含まれるもの:
1. エグゼクティブサマリー
2. KPI カード — 送信数、配信数、ユニーク開封数、ユニーククリック数、バウンス数、配信停止数
3. パフォーマンストレンドチャート（デュアル軸、自動粒度）
4. キャンペーンパフォーマンステーブル（送信数上位100件）
5. ジャーニーパフォーマンステーブル（送信数上位100件）

### キャンペーン詳細に含まれるもの:
1. エグゼクティブサマリー
2. KPI カード（フィルタ済み）
3. パフォーマンストレンドチャート
4. メール件名パフォーマンステーブル（送信数上位100件）

### 自動粒度ルール
| データスパン | 粒度 |
|---|---|
| 1〜34日 | 日次 |
| 35〜90日 | 週次 |
| 91日以上 | 月次 |

## トラブルシューティング

| エラー | 原因 | 解決策 |
|---|---|---|
| "No email delivery database found" | DB が未登録または名前が違う | `delivery_email_<ドメイン>` が KB として登録されているか確認 |
| "Missing required parameters" | キャンペーン詳細に識別子がない | campaign_id、journey_id、または subject を指定 |
| データが返されない | フィルタがデータにマッチしない | ID の存在確認、日付範囲の確認、フィルタを広げる |

## ライセンス
このエージェント設定は、Treasure Data の Engage サービスでの使用のために提供されています。

## サポート
これはリファレンス実装です。サポートは提供されません。
