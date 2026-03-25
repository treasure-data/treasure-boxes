# Report Specification: Campaign Details（日本語版）

> **注意**: このドキュメントは参考資料です。正式なレポート仕様は英語版（[knowledge_base_campaign_summary.md](./knowledge_base_campaign_summary.md)）を参照してください。

## 1. レポート概要
- purpose: "単一のキャンペーンまたはジャーニーの包括的なパフォーマンス分析を提供する（KPI、トレンド、メールタイトル別内訳を含む）。"
- source_tables:
    - "email_events"
    - "revenue"

## 2. フィルタ
- filter:
    - id: "campaign_id"
      type: "string"
      required: true
      exclusive_with: "journey_id"
- filter:
    - id: "journey_id"
      type: "string"
      required: true
      exclusive_with: "campaign_id"
- filter_notes: "campaign_id または journey_id が必要です。これらの ID のいずれかが提供された場合、日付範囲は不要です。レポートはその ID の利用可能なすべてのデータで実行されるべきです。"
- notes: "タイムスタンプカラム（event_timestamp, conversion_timestamp）は varchar 文字列です。date_parse(column, '%Y-%m-%d %H:%i:%s.%f') を使用して解析する必要があります。"

## 3. メトリクスに関する重要な注意事項

### ユニークカウント vs 総カウント
- **ユニークカウント**（プライマリメトリクス）: `COUNT(DISTINCT message_id)` を使用して、何回開封/クリックされたかに関わらず各メッセージを1回のみカウント。
- **総カウント**（補足情報）: `COUNT(*)` を使用して、同じメッセージの複数の開封/クリックを含むすべてのイベントをカウント。
- **率計算**: 膨張したメトリクスを避けるため、すべての率はユニークカウントを使用する必要があります（業界標準）。

### 識別子標準
- DISTINCT 集計には `message_id`（Amazon SES ユニークメッセージ ID）を使用。
- これにより Email Delivery Reports と業界のベストプラクティスとの整合性が確保されます。

### 時間粒度（トレンドコンポーネント用）

**重要: タイムスタンプ解析**
- event_timestamp と conversion_timestamp は TIMESTAMP 型ではなく VARCHAR 文字列です。
- これらのカラムを解析するには `date_parse(column, '%Y-%m-%d %H:%i:%s.%f')` を使用する必要があります。
- `CAST(column AS DATE)` または `CAST(column AS TIMESTAMP)` は使用しないでください - 失敗します。

SQL エージェントは、指定された campaign_id または journey_id の利用可能なデータの総日付範囲に基づいて時間粒度を動的に設定する必要があります：
- **<=20日**: 日次粒度
- **21-89日**: 週次粒度（月曜日開始）
- **>=90日**: 月次粒度

## 4. コンポーネント定義

### Component 1: Engagement KPIs
- component:
    - component_id: "kpi_summary_engagement"
    - component_type: "kpi_card_group"
    - title: "Engagement KPIs for {name} ({id})"
    - source_tables: ["email_events"]
    - metrics:
        - { metric_id: "sends", display_name: "Sends", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Send'", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Delivery'", format: "integer" }
        - { metric_id: "unique_opens", display_name: "Unique Opens", calculation: "COUNT(DISTINCT message_id) FROM email_events WHERE event_type = 'Open'", format: "integer", visual_priority: "primary" }
        - { metric_id: "total_opens", display_name: "Total Opens", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Open'", format: "integer", visual_priority: "tertiary", display_note: "補足情報" }
        - { metric_id: "unique_open_rate", display_name: "Unique Open Rate", calculation: "(COUNT(DISTINCT message_id) WHERE event_type = 'Open') / (COUNT(*) WHERE event_type = 'Delivery')", format: "percentage", visual_priority: "primary" }
        - { metric_id: "unique_clicks", display_name: "Unique Clicks", calculation: "COUNT(DISTINCT message_id) FROM email_events WHERE event_type = 'Click'", format: "integer", visual_priority: "primary" }
        - { metric_id: "total_clicks", display_name: "Total Clicks", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Click'", format: "integer", visual_priority: "tertiary", display_note: "補足情報" }
        - { metric_id: "unique_click_rate", display_name: "Unique Click Rate (CTR)", calculation: "(COUNT(DISTINCT message_id) WHERE event_type = 'Click') / (COUNT(*) WHERE event_type = 'Delivery')", format: "percentage", visual_priority: "primary" }
        - { metric_id: "bounces", display_name: "Bounces", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Bounce'", format: "integer" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "(COUNT(*) WHERE event_type = 'Bounce') / (COUNT(*) WHERE event_type = 'Send')", format: "percentage" }
        - { metric_id: "unsubscribes", display_name: "Unsubscribes", calculation: "COUNT(*) FROM email_events WHERE event_type = 'Complaint'", format: "integer" }
    - notes: |
        - Visual priority ガイダンス:
          * "primary": 目立つように表示（例: カウントは 32px ボールド、率は 24px ボールド）
          * "tertiary": 補足情報として表示（例: 13px レギュラー、"Total Opens: {value}"）
        - すべての率計算は膨張した率を避けるためにユニークカウント（COUNT DISTINCT message_id）を使用する必要があります。

### Component 2: Revenue KPIs
- component:
    - component_id: "kpi_summary_revenue"
    - component_type: "kpi_card_group"
    - title: "Revenue KPIs for {name} ({id})"
    - source_tables: ["revenue", "email_events"]
    - display_condition: "campaign_id でフィルタリングしている場合のみこのコンポーネントを表示。"
    - query_hints:
        - "ジャーニーの収益を取得するには、'revenue' と 'email_events' テーブルを 'campaign_id' で JOIN する必要があります。"
    - metrics:
        - { metric_id: "total_revenue", display_name: "Total Revenue", calculation: "revenue テーブルの attribution_type が 'direct' または 'contributed' の total_revenue の SUM", format: "currency", display_condition: "direct と contributed の両方の収益が存在する場合のみ表示。" }
        - { metric_id: "direct_revenue", display_name: "Direct Revenue", calculation: "revenue テーブルの attribution_type = 'direct' の total_revenue の SUM", format: "currency" }
        - { metric_id: "contributed_revenue", display_name: "Contributed Revenue", calculation: "revenue テーブルの attribution_type = 'contributed' の total_revenue の SUM", format: "currency" }

### Component 3: Performance by Email Title
- component:
    - component_id: "email_title_performance"
    - component_type: "table"
    - title: "Performance by Email Title"
    - source_tables: ["email_events"]
    - dimensions:
        - { id: "email_title", display_name: "Email Title" }
    - metrics:
        - { metric_id: "sends", display_name: "Sends", calculation: "COUNT(*) WHERE event_type = 'Send'", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "COUNT(*) WHERE event_type = 'Delivery'", format: "integer" }
        - { metric_id: "open_rate", display_name: "Open Rate", calculation: "(COUNT(*) WHERE event_type = 'Open') / (COUNT(*) WHERE event_type = 'Delivery')", format: "percentage" }
        - { metric_id: "ctr", display_name: "CTR (Click-Through Rate)", calculation: "(COUNT(*) WHERE event_type = 'Click') / (COUNT(*) WHERE event_type = 'Delivery')", format: "percentage" }
        - { metric_id: "bounces", display_name: "Bounces", calculation: "COUNT(*) WHERE event_type = 'Bounce'", format: "integer" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "(COUNT(*) WHERE event_type = 'Bounce') / (COUNT(*) WHERE event_type = 'Send')", format: "percentage" }
        - { metric_id: "unsubscribes", display_name: "Unsubscribes", calculation: "COUNT(*) WHERE event_type = 'Complaint'", format: "integer" }
    - sort_order: "sends DESC, email_title ASC"
    - notes: |
        - クエリ構築:
          1. email_events テーブルから email_title で直接 GROUP BY
          2. campaign_id または journey_id でフィルタ
          3. event_master テーブルの JOIN は不要
        - SQL エージェントは LIMIT 51 でクエリを実行してください。
        - 51行が返された場合、VIZ エージェントは次のノートを表示: 'Showing top 50 titles only. There may be additional titles not displayed.'
        - 最初の50行のみを表示。

### Component 4: Engagement Count Trend
- component:
    - component_id: "engagement_count_trend"
    - component_type: "line_chart"
    - title: "Engagement Trend (Counts)"
    - source_tables: ["email_events"]
    - y_axis_shared: true
    - visualization_hint: "mode: 'lines+markers'"
    - metrics:
        - { metric_id: "sends", display_name: "Sends", calculation: "COUNT(CASE WHEN event_type='Send' THEN 1 END)", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "COUNT(CASE WHEN event_type='Delivery' THEN 1 END)", format: "integer" }
        - { metric_id: "unique_opens", display_name: "Unique Opens", calculation: "COUNT(DISTINCT CASE WHEN event_type='Open' THEN message_id END)", format: "integer", visual_priority: "primary" }
        - { metric_id: "unique_clicks", display_name: "Unique Clicks", calculation: "COUNT(DISTINCT CASE WHEN event_type='Click' THEN message_id END)", format: "integer", visual_priority: "primary" }
        - { metric_id: "bounce_count", display_name: "Bounces", calculation: "COUNT(CASE WHEN event_type='Bounce' THEN 1 END)", format: "integer" }
        - { metric_id: "complaint_count", display_name: "Complaints", calculation: "COUNT(CASE WHEN event_type='Complaint' THEN 1 END)", format: "integer" }
    - notes: |
        - このコンポーネントは 'event_timestamp' カラムに基づいています。
        - ゼロパディングは不要です。
        - 時間粒度はキャンペーン/ジャーニーデータの総日付範囲によって決定されます（セクション3を参照）。
        - すべてのメトリクスは膨張したカウントを避けるため、開封とクリックに COUNT DISTINCT message_id を使用します。

### Component 5: Conversions and Revenue Trend
- component:
    - component_id: "conversions_trend"
    - component_type: "line_chart"
    - title: "Conversions & Revenue Trend"
    - source_tables: ["revenue", "email_events"]
    - y_axis_shared: false
    - visualization_hint: "mode: 'lines+markers', dual y-axis (left: count, right: currency)"
    - display_condition: "campaign_id でフィルタリングしている場合のみ表示。"
    - metrics:
        - { metric_id: "conversions", display_name: "Conversions", calculation: "COUNT(DISTINCT conversion_id) FROM revenue", format: "integer", y_axis: "left" }
        - { metric_id: "direct_revenue", display_name: "Direct Revenue", calculation: "SUM(total_revenue) FROM revenue WHERE attribution_type = 'direct'", format: "currency", y_axis: "right" }
        - { metric_id: "contributed_revenue", display_name: "Contributed Revenue", calculation: "SUM(total_revenue) FROM revenue WHERE attribution_type = 'contributed'", format: "currency", y_axis: "right" }
        - { metric_id: "total_revenue", display_name: "Total Revenue", calculation: "SUM(total_revenue) FROM revenue WHERE attribution_type IN ('direct', 'contributed')", format: "currency", y_axis: "right" }
    - notes: |
        - このコンポーネントは 'conversion_timestamp' カラムに基づいています。
        - ゼロパディングは不要です。
        - 時間粒度はキャンペーン/ジャーニーデータの総日付範囲によって決定されます（セクション3を参照）。
        - デュアル y 軸を使用: カウントメトリクス（コンバージョン）は左、通貨メトリクス（収益）は右。
        - このコンポーネントは曜日パターンとキャンペーンタイミング効果の特定に役立ちます。

## 5. コンポーネントレンダリング順序

最終出力は以下の順序でコンポーネントをレンダリングする必要があります：

1. Title
2. Summary（データドリブンなインサイト）
3. kpi_summary_engagement
4. kpi_summary_revenue（campaign_id とデータが存在する場合）
5. engagement_count_trend
6. conversions_trend（campaign_id とデータが存在する場合）
7. email_title_performance
