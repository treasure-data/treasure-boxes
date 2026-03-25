# Email Delivery Reporter Agent

## 概要

このエージェントは、Treasure Data の Engage サービス向けにメール配信レポートを生成します。PlazmaDB のメール配信ログを自動的に分析し、Trino に対して SQL クエリを実行し、ビジュアライゼーションとインサイトを含むインタラクティブなダッシュボードを生成します。

エージェントは2種類のレポートを作成できます：
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

## 前提条件

### 必要な PlazmaDB データベース

このエージェントは、Engage のメール配信ログを含む PlazmaDB データベースが必要です。

**重要**: データベース名は特定のパターンに従います：
```
delivery_email_<メールドメイン>
```

`<メールドメイン>` は、ドット（`.`）をアンダースコア（`_`）に置き換えたメールドメインです。

**例:**
- メールドメイン: `example.com` → データベース: `delivery_email_example_com`
- メールドメイン: `my-company.co.jp` → データベース: `delivery_email_my_company_co_jp`

**注意**: 各ユーザーのデータベース名はメールドメインに基づいて異なります。このエージェントを使用する前に、正しいデータベースがプロジェクトのナレッジベースとして登録されていることを確認してください。

### 必要なテーブル

データベースには以下のテーブルが含まれている必要があります：

1. **events** (またはエイリアス: email_events)
   - メールイベントログを含む: Send, Delivery, Open, Click, Bounce, Complaint, DeliveryDelay
   - 主要カラム: `time`, `timestamp`, `event_type`, `email_sender_id`, `email_template_id`, `subject`, `custom_event_id`, `test_mode`, `message_id`, `campaign_id`, `journey_id`

2. **error_events**
   - 送信前の失敗を含む（レンダリングエラー、ランタイムエラー）
   - 主要カラム: `timestamp`, `error_type`, `error_message`, `custom_event_id`

3. **subscription_events** (またはエイリアス: email_subscription_events)
   - オプトアウト/配信停止イベントを含む
   - 主要カラム: `profile_identifier_value`, `campaign_id`, `campaign_name`, `action`, `action_source`, `received_time`, `time`

## セットアップ手順

### 1. PlazmaDB データベースをナレッジベースとして登録

1. AI Agent Foundry UI でプロジェクトを作成
2. ナレッジベース設定に移動
3. PlazmaDB データベース（`delivery_email_<あなたのドメイン>`）を追加
4. データベース接続がアクティブであることを確認
5. このナレッジベースは `List_columns` と `Query_data_directly` ツールで使用されます（ステップ4で設定）

### 2. エージェントを作成

1. プロジェクト内に新しいエージェントを作成
2. [system_prompt.md](./system_prompt.md) からシステムプロンプトをコピーしてシステムプロンプトフィールドに貼り付け
3. エージェント設定を保存

### 3. レポート仕様をテキストナレッジベースとして追加

1. プロジェクト内に新しいテキストナレッジベースを作成
2. [knowledge_base.md](./knowledge_base.md) からコンテンツをコピーしてナレッジベースに貼り付け
3. このナレッジベースをエージェントにリンク（ステップ4で設定する `read_report_specs` ツール経由でアクセスされます）

### 4. ツールを設定

エージェントに以下のツールを設定します。各ツールには以下に詳述する特定の設定が必要です。

#### 4.1 データアクセスツール

##### List_columns
- **Function name**: `List_columns`
- **Function description**: テーブルスキーマを検出します。データベース内のテーブルのカラム名、型、コメントを返します。
- **Target**: Knowledge Base
- **Target knowledge base**: `delivery_email_<DOMAIN_NAME>`
- **Target function**: List columns

##### Query_data_directly
- **Function name**: `Query_data_directly`
- **Function description**: Plazma DB に対して SQL クエリを実行します。最大100行を返します。GROUP BY 集計を使用してください。SELECT * は使用しないでください。結果に [TRUNCATED] が含まれる場合は、OFFSET と LIMIT を使用してページネーションを行います。
- **Target**: Knowledge Base
- **Target knowledge base**: `delivery_email_<DOMAIN_NAME>`
- **Target function**: Query data directly (Presto SQL)

##### read_report_specs
- **Function name**: `read_report_specs`
- **Function description**: レポートの仕様
- **Target**: Knowledge Base
- **Target knowledge base**: Email Delivery Report Specs
- **Target function**: Read

#### 4.2 出力ツール

##### renderReactApp
- **Output name**: `renderReactApp`
- **Function name**: `renderReactApp`
- **Function description**: Tailwind CSS を使用して React コンポーネントを生成します。環境制約: 1. チャート: react-plotly.js のみがインストールされています。recharts はインストールされていません（インポートしないでください）。2. アイコン: lucide-react はインストールされていません。インライン <svg> タグのみを使用してください。3. UI: 静的ビューのみ。<button> または <a> タグは使用しないでください（ダウンロード/詳細アクションなし）。単一ファイル、export default。
- **Output Type**: Artifact
- **Artifact content type**: React

##### text_in_form
- **Output name**: `text_in_form`
- **Function name**: `text_in_form`
- **Function description**: renderMarkdown エラーメッセージのみを返したい場合に呼び出します
- **Output Type**: Artifact
- **Artifact content type**: Text

##### :plotly: (new_plot)
- **Output name**: `:plotly:`
- **Function name**: `new_plot`
- **Function description**: Plotly.js を使用してチャートをレンダリングし、分析結果のビジュアライゼーションを提供します。
  - カラースキームを使用: ["B4E3E3", "ABB3DB", "D9BFDF", "F8E1B0", "8FD6D4", "828DCA", "C69ED0", "F5D389", "6AC8C6", "5867B8", "B37EC0", "F1C461", "44BAB8", "2E41A6", "8CC97E", "A05EB0"]
  - 3つ以上のカテゴリを持つチャートには、updatemenus を積極的に使用
  - 複数の分析を要約する場合、Plotly のグリッドレイアウト（例: grid: {rows: 2, columns: 2, pattern: 'independent'}）を使用して関連するチャートを単一のダッシュボードに結合し、要素が重ならないようにする
  - テキストの重複を防ぐ:
    * 十分なマージンを含める: {l: 80, r: 80, t: 100, b: 80}
    * 小さなセグメント（<5%）の円グラフには textinfo: 'none' を使用し、ラベルの代わりに凡例に依存
    * 最小ダッシュボード寸法を設定: height: 600, width: 1000
    * グリッドレイアウトには、0.1 ギャップの広いドメインスペーシングを使用: [0, 0.45] と [0.55, 1]
- **Output Type**: Custom
- **Artifact content type**:
  ```json
  {
    "type": "object",
    "properties": {
      "data": {
        "type": "array",
        "description": "Plotly.js data JSON objects",
        "items": {
          "type": "object"
        }
      },
      "layout": {
        "type": "object",
        "description": "Plotly.js layout JSON object"
      }
    },
    "required": ["data"]
  }
  ```

## 使用方法

### 全体サマリーレポート

すべてのキャンペーンとジャーニーにわたる包括的なサマリーレポートを生成します。

**必須パラメータ:**
- `date_range`: レポート期間の開始日と終了日
  - 形式: `start_date: 'YYYY-MM-DD', end_date: 'YYYY-MM-DD'`
  - 省略時: データベースの全データ範囲を使用
- `language`: レポート言語
  - オプション: `'en'`（英語）または `'ja'`（日本語）
  - デフォルト: `'en'`

**オプションパラメータ:**
- `campaign_id`: 特定のキャンペーンIDでフィルタ
- `journey_id`: 特定のジャーニーIDでフィルタ
- `subject`: メール件名でフィルタ（大文字小文字を区別しない部分一致）

**リクエスト例:**

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

```
Show me Q4 2024 email performance for campaign ABC123.
date_range: { start_date: '2024-10-01', end_date: '2024-12-31' }
campaign_id: 'ABC123'
language: 'en'
```

上記はチャット UI でのユーザープロンプトの例ですが、上記の必須フィールドを含む入力 `Input form` を作成することで、ユーザープロンプトに慣れていないユーザーにも機能を提供できます。


### キャンペーン詳細レポート

特定のキャンペーン、ジャーニー、または件名の詳細レポートを生成します。

**必須パラメータ:**
- **以下のいずれか1つ以上**:
  - `campaign_id`: 特定のキャンペーン識別子
  - `journey_id`: 特定のジャーニー識別子
  - `subject`: メール件名フィルタ（大文字小文字を区別しない部分一致）

**オプションパラメータ:**
- `date_range`: 開始日と終了日
  - 省略時: 指定されたキャンペーン/ジャーニーの全データ範囲を使用
- `language`: レポート言語（`'en'` または `'ja'`）
  - デフォルト: `'en'`

**リクエスト例:**

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

```
Show me all emails with "Black Friday" in the subject from November 2024.
subject: 'Black Friday'
date_range: { start_date: '2024-11-01', end_date: '2024-11-30' }
language: 'en'
```

```
Analyze campaign ABC123 during December 2024 and January 2025.
campaign_id: 'ABC123'
date_range: { start_date: '2024-12-01', end_date: '2025-01-31' }
language: 'en'
```


## レポートコンポーネント

### 全体サマリーレポートに含まれるもの:

1. **エグゼクティブサマリー**: 主要なインサイトを含むデータドリブンな説明
2. **KPI カード**:
   - 総送信数
   - 配信数 & 配信率
   - ユニーク開封数 & 開封率（+ 総開封数）
   - ユニーククリック数 & クリック率（+ 総クリック数）
   - バウンス数 & バウンス率
   - 配信停止数 & 配信停止率
3. **パフォーマンストレンドチャート**: 時間経過に伴うボリュームとレートメトリクスを示すデュアル軸折れ線グラフ
4. **キャンペーンパフォーマンステーブル**: 送信数上位100キャンペーン
5. **ジャーニーパフォーマンステーブル**: 送信数上位100ジャーニー

### キャンペーン詳細レポートに含まれるもの:

1. **エグゼクティブサマリー**: キャンペーン固有のインサイト
2. **KPI カード**: 全体サマリーと同じメトリクス、キャンペーン/ジャーニー/件名でフィルタ
3. **パフォーマンストレンドチャート**: キャンペーン固有の時系列トレンド
4. **メール件名パフォーマンステーブル**: 送信数上位100件名

## 重要な注意事項

### データベース名の依存関係

**重要**: このエージェントは動的なデータベース検出を使用し、データベース名をハードコードしていません。エージェントは以下を実行します：

1. `SHOW SCHEMAS LIKE 'delivery_email_%'` を実行してデータベースを検索
2. 最初にマッチしたスキーマを自動的に使用
3. マッチするデータベースが見つからない場合はエラーを返す

**必要なアクション**: このエージェントを使用する前に、`delivery_email_<ドメイン>` データベースが適切に登録されていることを確認してください。

### データ粒度

時系列チャートは日付範囲に基づいて粒度を自動調整します：
- **1-34日**: 日次集計
- **35-90日**: 週次集計
- **91日以上**: 月次集計

### テーブル制限

キャンペーン、ジャーニー、件名のテーブルは送信数上位100件を表示します。100件を超えるアイテムが存在する場合、警告バナーが表示されます。

### メトリクスの計算

**重要**: すべての開封率とクリック率は、膨張した率を避けるため**ユニークカウント**（message_id あたり1）を使用します。総カウントは補足情報としてのみ表示されます。

## トラブルシューティング

### "No email delivery database found"（メール配信データベースが見つかりません）

**原因**: エージェントがパターン `delivery_email_%` にマッチするデータベースを見つけられない

**解決策**:
1. データベース名がパターン `delivery_email_<ドメイン>` に従っているか確認
2. データベースが Agent Framework に登録されていることを確認
3. データベース接続ステータスを確認

### "Missing required parameters"（必須パラメータが不足しています）

**原因**: キャンペーン詳細レポートには {campaign_id, journey_id, subject} のいずれか1つ以上が必要

**解決策**: リクエストに少なくとも1つの識別子を提供

### データが返されない

**原因**: 指定されたフィルタがデータにマッチしない可能性がある

**解決策**:
1. campaign_id、journey_id、または subject の値がデータに存在するか確認
2. 日付範囲にメールが送信された期間が含まれているか確認
3. フィルタを広げてみる

## ライセンス

このエージェント設定は、Treasure Data の Engage サービスでの使用のために提供されています。

## サポート

- これは独自のエージェントを構築するためのリファレンスであり、サポートは提供されません。
