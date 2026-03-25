# Email Delivery Report 仕様（日本語版）

> **注意**: このドキュメントは参考資料です。正式なレポート仕様は英語版（[knowledge_base.md](./knowledge_base.md)）を参照してください。

このドキュメントは、Engage Email 配信レポーティングのレポート仕様を定義します。
全体サマリーとキャンペーン/ジャーニーサマリーの2つのレポートバリアントをカバーします。

---

## 共通用語

**ボリュームメトリクス:**
- `sends`: 総メール送信試行回数（event_type = 'Send'）。
- `deliveries`: 正常に配信されたメール（event_type = 'Delivery'）。
- `delivery_rate`: deliveries / sends

**エンゲージメントメトリクス（ユニークベース）:**
- `unique_opens`: event_type = 'Open' の異なる message_id カウント
- `total_opens`: 総開封イベントカウント（参考用）
- `unique_open_rate`: unique_opens / deliveries
- `unique_clicks`: event_type = 'Click' の異なる message_id カウント
- `total_clicks`: 総クリックイベントカウント（参考用）
- `unique_click_rate`: unique_clicks / deliveries

**品質メトリクス:**
- `bounces`: 配信失敗（event_type = 'Bounce'）。
- `bounce_rate`: bounces / sends
- `complaints`: スパム苦情（event_type = 'Complaint'）。
- `unsubscribes`: オプトアウトイベント（subscription_events の action='opt-out' 行）。
- `unsubscribe_rate`: unsubscribes / deliveries

**重要**: すべての開封率とクリック率は、膨張した率を避けるためにユニークカウント（message_id あたり1）を使用する必要があります。総カウントは補足情報としてのみ表示されます。

---

## 共通 SQL パターン

### events テーブルからのメトリクス集計

```sql
SUM(CASE WHEN event_type = 'Send' THEN 1 ELSE 0 END)       -- sends
SUM(CASE WHEN event_type = 'Delivery' THEN 1 ELSE 0 END)   -- deliveries
SUM(CASE WHEN event_type = 'Open' THEN 1 ELSE 0 END)       -- total_opens
COUNT(DISTINCT CASE WHEN event_type = 'Open' THEN message_id END)  -- unique_opens
SUM(CASE WHEN event_type = 'Click' THEN 1 ELSE 0 END)      -- total_clicks
COUNT(DISTINCT CASE WHEN event_type = 'Click' THEN message_id END) -- unique_clicks
SUM(CASE WHEN event_type = 'Bounce' THEN 1 ELSE 0 END)     -- bounces
SUM(CASE WHEN event_type = 'Complaint' THEN 1 ELSE 0 END)  -- complaints
```

### subscription_events テーブルからの配信停止
```sql
COUNT(*) WHERE action = 'opt-out'
```

### 率計算（除算の安全性）
```sql
CAST(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)  -- delivery_rate

CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)  -- unique_open_rate

CAST(COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)  -- unique_click_rate

CAST(SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)  -- bounce_rate

CAST(COUNT(*) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)  -- unsubscribe_rate (from subscription_events)
```

### 日付フィルタリング
```sql
DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ')) BETWEEN DATE '{start_date}' AND DATE '{end_date}'
```

### 時間集計ポリシー
email_events からの `DATE(timestamp)` のデータスパンに基づく：

| データスパン | 粒度 | date_key 式 |
|-----------|-------------|---------------------|
| 1-34日 | 日次 | `DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ'))` |
| 35-90日 | 週次 | `date_trunc('week', DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ')))` |
| 91日以上 | 月次 | `date_trunc('month', DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ')))` |

---

## レポート仕様: DeliveryOverallSummary

### 概要
- **目的**: 期間全体の配信 KPI、トレンド、キャンペーン/ジャーニーリスト（収益やコンバージョンなし）。
- **ソーステーブル**: events, subscription_events
- **ビジュアルデザイン**: 絵文字アイコン、グラデーション背景、拡張チャート付きのモダンでカラフルなカード

### フィルタ

| Filter ID | Type | Required | Notes |
|-----------|------|----------|-------|
| date_range | date | YES | start_date と end_date は必須。不足している場合: 利用可能な最小/最大日付を返し、全範囲を使用。範囲が365日を超える場合: 受け入れるが警告。 |
| campaign_id | string | no | オプションの追加フィルタ。すべてのコンポーネントに適用。 |
| journey_id | string | no | オプションの追加フィルタ。すべてのコンポーネントに適用。 |
| subject | string | no | メール件名の大文字小文字を区別しない部分一致。 |

**注意**: campaign_id と journey_id は events テーブルのネイティブカラムです。

### コンポーネント

#### Component: executive_summary
- **component_type**: text_summary
- **title**: "📊 Executive Summary"
- **content**: 以下を含むデータドリブンなナラティブサマリー:
  - 総期間（日数）
  - 総送信数と配信率
  - エンゲージメントメトリクス（ユニーク開封数、総開封数、ユニーククリック数、総クリック数と率）
  - 品質メトリクス（バウンス、苦情、配信停止と率）
  - 注目すべきパターン（例: 大量送信、ピーク期間）
- **style**:
  - 微妙な影付きの白背景
  - 16px フォントサイズ、1.8 行間
  - カラーコーディング付きの主要数値のボールドハイライト
  - 丸い角（12px ボーダーラディウス）

#### Component: kpi_summary
- **component_type**: kpi_card_group
- **title**: "📈 Key Performance Indicators"
- **layout**: レスポンシブグリッド（auto-fit, minmax(220px, 1fr)）
- **card_design**:
  - グラデーション背景（カラー + 15% 不透明度から白へ）
  - 丸い角（12px）
  - 深みのあるボックスシャドウ
  - 各メトリクスカテゴリの絵文字アイコン
  - プライマリメトリクス: 32px ボールド、カラー付き
  - セカンダリメトリクス: 24px ボールド、グレー
  - ターシャリー情報: 13px、グレー（総カウント用）
  - プライマリとセカンダリの間の区切り線
  - ラベル: 13px、大文字、レタースペーシング

**メトリクス:**

| metric_id | display_name | emoji | calculation | format | color | card_grouping |
|-----------|--------------|-------|-------------|--------|-------|---------------|
| sends | Total Sends | 📤 | `SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END)` | integer | #44BAB8 | sends_only |
| deliveries | Delivered | ✅ | `SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END)` | integer | #44BAB8 | deliveries_with_rate |
| delivery_rate | Delivery Rate | ✅ | `CAST(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)` | percentage | #44BAB8 | deliveries_with_rate |
| unique_opens | Unique Opens | 👁️ | `COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END)` | integer | #5867B8 | opens_with_rate |
| unique_open_rate | Unique Open Rate | 👁️ | `CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage | #5867B8 | opens_with_rate |
| total_opens | Total Opens | 👁️ | `SUM(CASE WHEN event_type='Open' THEN 1 ELSE 0 END)` | integer | #5867B8 | opens_tertiary |
| unique_clicks | Unique Clicks | 🖱️ | `COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END)` | integer | #B37EC0 | clicks_with_rate |
| unique_click_rate | Unique Click Rate | 🖱️ | `CAST(COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage | #B37EC0 | clicks_with_rate |
| total_clicks | Total Clicks | 🖱️ | `SUM(CASE WHEN event_type='Click' THEN 1 ELSE 0 END)` | integer | #B37EC0 | clicks_tertiary |
| bounces | Total Bounces | ⚠️ | `SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END)` | integer | #e74c3c | bounces_with_rate |
| bounce_rate | Bounce Rate | ⚠️ | `CAST(SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)` | percentage | #e74c3c | bounces_with_rate |
| unsubscribes | Total Unsubscribes | 🚫 | `COUNT(*) FROM subscription_events WHERE action='opt-out'` | integer | #95a5a6 | unsubscribes_with_rate |
| unsubscribe_rate | Unsubscribe Rate | 🚫 | `CAST(COUNT(*) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage | #95a5a6 | unsubscribes_with_rate |

**カードグルーピングロジック:**
- **Sends カード**: 送信数のみ表示（セカンダリメトリクスなし）
- **Deliveries カード**: プライマリ = deliveries (integer), セカンダリ = delivery_rate (percentage)
- **Unique Opens カード**: プライマリ = unique_opens (integer), セカンダリ = unique_open_rate (percentage), ターシャリー = "Total Opens: {total_opens}"
- **Unique Clicks カード**: プライマリ = unique_clicks (integer), セカンダリ = unique_click_rate (percentage), ターシャリー = "Total Clicks: {total_clicks}"
- **Bounces カード**: プライマリ = bounces (integer), セカンダリ = bounce_rate (percentage)
- **Unsubscribes カード**: プライマリ = unsubscribes (integer), セカンダリ = unsubscribe_rate (percentage)

#### Component: performance_trend
- **component_type**: dual_axis_line_chart
- **title**: "📉 Monthly Performance Trend"（粒度に基づいて調整）
- **time_column**: date_key（集計ポリシーに従って導出）
- **zero_padding**: 必須（SEQUENCE と LEFT JOIN を使用）
- **chart_design**:
  - 幅: 1300px, 高さ: 650px
  - マージン: {l:80, r:100, t:60, b:80}
  - プロット背景: #fafafa
  - ペーパー背景: 白
  - グリッドカラー: #e8e8e8
  - 線幅: 3px
  - マーカーサイズ: 8px
  - 送信数ラインの下の領域を塗りつぶし（tozeroy、20% 不透明度）
  - 凡例: 水平、チャート下部中央
  - ホバーモード: x 統一

**レイアウト設定:**
- **yaxis（左）**: ボリュームメトリクス
- **yaxis2（右）**: 率メトリクス

**メトリクス:**

| metric_id | display_name | calculation | axis | format | color | style |
|-----------|--------------|-------------|------|--------|-------|-------|
| sends | Sends | `SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END)` | left | integer | #44BAB8 | 実線 + 塗りつぶし |
| deliveries | Deliveries | `SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END)` | left | integer | #8FD6D4 | 実線 |
| unique_clicks | Unique Clicks | `COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END)` | left | integer | #B37EC0 | 実線 |
| unique_open_rate | Unique Open Rate (%) | `CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0) * 100` | right | percentage | #F1C461 | 点線 + ダイヤモンドマーカー |

**ゼロパディング付きトレンドの SQL パターン:**

```sql
WITH date_range AS (
  SELECT
    CAST(MIN(DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ'))) AS DATE) as s,
    CAST(MAX(DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ'))) AS DATE) as e
  FROM events
  WHERE [date_filter]
),
time_series AS (
  SELECT date_trunc('month', t.dt) as month_start
  FROM date_range
  CROSS JOIN UNNEST(SEQUENCE(s, e, INTERVAL '1' DAY)) AS t(dt)
  GROUP BY date_trunc('month', t.dt)
),
monthly_metrics AS (
  SELECT
    date_trunc('month', DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ'))) as month_start,
    SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END) as sends,
    SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END) as deliveries,
    COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) as unique_opens,
    COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) as unique_clicks
  FROM events
  WHERE [date_filter]
  GROUP BY date_trunc('month', DATE(date_parse(timestamp, '%Y-%m-%dT%H:%i:%s.%fZ')))
)
SELECT
  CAST(ts.month_start AS VARCHAR) as month_start,
  COALESCE(mm.sends, 0) as sends,
  COALESCE(mm.deliveries, 0) as deliveries,
  COALESCE(mm.unique_clicks, 0) as unique_clicks,
  CAST(COALESCE(mm.unique_opens, 0) AS DOUBLE) / NULLIF(COALESCE(mm.deliveries, 0), 0) as unique_open_rate
FROM time_series ts
LEFT JOIN monthly_metrics mm ON ts.month_start = mm.month_start
ORDER BY ts.month_start
```

#### Component: campaign_performance_list
- **component_type**: table
- **title**: "📋 All Campaigns Performance"
- **source_tables**: events（ネイティブ campaign_id と campaign_name カラムを使用）
- **dimensions**:
  - campaign_id（キャンペーン ID）
  - campaign_name（キャンペーン名）
- **metrics**:

| metric_id | display_name | calculation | format |
|-----------|--------------|-------------|--------|
| sends | Sends | `SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END)` | integer |
| deliveries | Deliveries | `SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END)` | integer |
| unique_opens | Unique Opens | `COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END)` | integer |
| unique_open_rate | Unique Open Rate | `CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage |
| unique_click_rate | Unique Click Rate | `CAST(COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage |
| bounce_rate | Bounce Rate | `CAST(SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)` | percentage |

- **orderby_clause_template**: `ORDER BY SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END) DESC, campaign_id DESC`
- **limit**: 100
- **notes**:
  - 送信数でソートされた上位100キャンペーンを表示
  - 結果カウントが100の場合、実行: `SELECT COUNT(DISTINCT campaign_id) FROM events WHERE [filters] AND campaign_id IS NOT NULL`
  - 総カウントが100を超える場合、警告を表示: "⚠️ Showing top 100 of {total_count} campaigns. Results are ordered by send volume (highest first)."
  - campaign_id データが存在しない場合、このコンポーネントをスキップ

#### Component: journey_performance_list
- **component_type**: table
- **title**: "🚀 All Journeys Performance"
- **source_tables**: events（ネイティブ journey_id カラムを使用）
- **dimensions**:
  - journey_id（ジャーニー ID）
- **metrics**: campaign_performance_list と同じ
- **orderby_clause_template**: `ORDER BY SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END) DESC, journey_id DESC`
- **limit**: 100
- **notes**:
  - 送信数でソートされた上位100ジャーニーを表示
  - 結果カウントが100の場合、実行: `SELECT COUNT(DISTINCT journey_id) FROM events WHERE [filters] AND journey_id IS NOT NULL`
  - 総カウントが100を超える場合、警告を表示: "⚠️ Showing top 100 of {total_count} journeys. Results are ordered by send volume (highest first)."
  - journey_id データが存在しない場合、このコンポーネントをスキップ

---

## レポート仕様: DeliveryCampaignSummary

### 概要
- **目的**: 単一のキャンペーン、ジャーニー、または件名フィルタスライスの詳細な配信パフォーマンスサマリー（収益なし）。
- **ソーステーブル**: events, subscription_events
- **ビジュアルデザイン**: DeliveryOverallSummary と同じ

### フィルタ

| Filter ID | Type | Required | Notes |
|-----------|------|----------|-------|
| campaign_id | string | no | journey_id と相互排他的。 |
| journey_id | string | no | campaign_id と相互排他的。 |
| subject | string | no | 大文字小文字を区別しない部分一致。 |
| date_range | date | no | オプションの日付範囲フィルタ。 |

**フィルタルール**: {campaign_id, journey_id, subject} のいずれか1つ以上が必須。複数提供された場合、AND で結合。

### コンポーネント

#### Component: executive_summary
- **component_type**: text_summary
- **title**: "📊 Executive Summary for {name}"
- **content**: 以下を含むデータドリブンなナラティブサマリー:
  - キャンペーン/ジャーニー/件名の識別
  - 総期間（日数）
  - 総送信数と配信率
  - エンゲージメントメトリクス（ユニーク開封数、総開封数、ユニーククリック数、総クリック数と率）
  - 品質メトリクス（バウンス、苦情、配信停止と率）
  - このキャンペーン/ジャーニー固有の注目すべきパターン

#### Component: kpi_summary_engagement
- **component_type**: kpi_card_group
- **title**: "📈 Key Performance Indicators for {name}"
- **source_tables**: events, subscription_events
- **metrics**: DeliveryOverallSummary kpi_summary と同じ構造
- **notes**: すべてのメトリクスは campaign_id OR journey_id OR subject でフィルタ

#### Component: performance_trend
- **component_type**: dual_axis_line_chart
- **title**: "📉 Delivery Trend for {name}"
- **time_column**: date_key（集計ポリシーに従って導出）
- **metrics**: DeliveryOverallSummary performance_trend と同じ
- **notes**:
  - データスパンに基づいて集計ポリシー（日次/週次/月次）を使用
  - ゼロパディング推奨だが厳密には必須ではない

#### Component: email_subject_performance_list
- **component_type**: table
- **title**: "📧 All Email Subjects Performance"
- **source_tables**: events
- **dimensions**:
  - subject（メール件名）
  - オプション: email_template_id
- **metrics**:

| metric_id | display_name | calculation | format |
|-----------|--------------|-------------|--------|
| sends | Sends | `SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END)` | integer |
| deliveries | Deliveries | `SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END)` | integer |
| unique_opens | Unique Opens | `COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END)` | integer |
| unique_open_rate | Unique Open Rate | `CAST(COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage |
| unique_click_rate | Unique Click Rate | `CAST(COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Delivery' THEN 1 ELSE 0 END), 0)` | percentage |
| bounces | Bounces | `SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END)` | integer |
| bounce_rate | Bounce Rate | `CAST(SUM(CASE WHEN event_type='Bounce' THEN 1 ELSE 0 END) AS DOUBLE) / NULLIF(SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END), 0)` | percentage |
| unsubscribes | Unsubscribes | `COUNT(*) FROM subscription_events WHERE ...` | integer |

- **orderby_clause_template**: `ORDER BY SUM(CASE WHEN event_type='Send' THEN 1 ELSE 0 END) DESC, subject ASC`
- **limit**: 100
- **notes**:
  - 送信数でソートされた上位100件名を表示
  - 結果カウントが100の場合、実行: `SELECT COUNT(DISTINCT subject) FROM events WHERE [filters]`
  - 総カウントが100を超える場合、警告を表示: "⚠️ Showing top 100 of {total_count} email subjects. Results are ordered by send volume (highest first)."
  - COALESCE を使用して NULL を 0 に変換
  - 指定された campaign_id/journey_id/subject でフィルタ

---

## デザインシステム

### カラーパレット
```javascript
const colors = [
  "#44BAB8",  // ティール（送信、配信）
  "#5867B8",  // ブルー（開封）
  "#B37EC0",  // パープル（クリック）
  "#F1C461",  // イエロー（率）
  "#8FD6D4",  // ライトティール
  "#828DCA",  // ライトブルー
  "#C69ED0",  // ライトパープル
  "#F5D389",  // ライトイエロー
  "#e74c3c",  // レッド（バウンス、エラー）
  "#95a5a6"   // グレー（配信停止）
];
```

### タイポグラフィ
- **フォントファミリー**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif
- **タイトル**: 32px, ボールド (700)
- **セクションヘッダー**: 20px, セミボールド (600)
- **カードタイトル**: 14px, セミボールド (600), 大文字, レタースペーシング 0.5px
- **プライマリ値**: 32px, ボールド
- **セカンダリ値**: 24px, ボールド
- **ターシャリー情報**: 13px, レギュラー
- **本文テキスト**: 16px, 行間 1.8
- **ラベル**: 13-14px

### スペーシング
- **ページパディング**: 40px
- **セクション margin-bottom**: 32px
- **カードギャップ**: 24px
- **カードパディング**: 24-32px
- **ボーダーラディウス**: 12px

### シャドウ & ボーダー
- **カードシャドウ**: 0 4px 6px rgba(0,0,0,0.1)
- **セクションシャドウ**: 0 2px 8px rgba(0,0,0,0.08)
- **ボーダー**: 1px solid #e8e8e8

---

## 実装ノート

1. **率には常にユニークカウントを使用**: 総イベントカウントを使用して open_rate や click_rate を計算しないでください
2. **ユニークと総の両方を表示**: ユニークをプライマリメトリクスとして表示し、総を補足情報として表示
3. **警告付きの制限リスト**: キャンペーン、ジャーニー、件名のテーブルは上位100行を表示し、それ以上存在する場合は警告を表示
4. **一貫したフォーマット**: すべての数値表示に formatNumber() ヘルパーを使用
5. **グレースフル・デグレデーション**: コンポーネントにデータがない場合、ノート付きでスキップ
