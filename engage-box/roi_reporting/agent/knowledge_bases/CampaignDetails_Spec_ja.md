# Report Specification: Campaign Details（日本語版）

> **注意**: このドキュメントは参考資料です。正式なレポート仕様は英語版（[CampaignDetails_Spec.md](./CampaignDetails_Spec.md)）を参照してください。

## 1. レポート概要
- purpose: "単一のキャンペーンまたはジャーニーの包括的なパフォーマンス分析を提供し、KPI、トレンド、メール件名別の内訳を含む。"
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
- filter_notes: "campaign_idまたはjourney_idが必要です。これらのIDの一つが提供された場合、日付範囲は不要です。レポートはそのIDの利用可能なすべてのデータで実行されるべきです。"
- notes: "タイムスタンプカラム（event_timestamp, conversion_timestamp）はvarchar文字列です。date_parse(column, '%Y-%m-%d %H:%i:%s.%f')を使用して解析する必要があります。"

## 3. メトリクスに関する重要な注意事項

### ユニークカウント vs 総カウント
- **ユニークカウント**（主要メトリクス）: `COUNT(DISTINCT message_id)`を使用して、開封/クリックされた回数に関わらず各メッセージを1回のみカウントします。
- **総カウント**（補足情報）: `COUNT(*)`を使用して、同じメッセージの複数回の開封/クリックを含むすべてのイベントをカウントします。
- **率計算**: すべての率はユニークカウントを使用する必要があります（業界標準）。

### 識別子標準
- DISTINCT集計には`message_id`（Amazon SESユニークメッセージID）を使用します。
- これによりEmail Delivery Reportsおよび業界ベストプラクティスとの一貫性が保証されます。

### 時間粒度（トレンドコンポーネント用）

**重要: タイムスタンプ解析**
- event_timestampとconversion_timestampはVARCHAR文字列であり、TIMESTAMPタイプではありません。
- これらのカラムを解析するには`date_parse(column, '%Y-%m-%d %H:%i:%s.%f')`を使用する必要があります。
- `CAST(column AS DATE)`または`CAST(column AS TIMESTAMP)`は使用しないでください - これらは失敗します。

SQLエージェントは、指定されたcampaign_idまたはjourney_idの利用可能なデータの総日付範囲に基づいて時間粒度を動的に設定する必要があります：
- **<=20日**: 日次粒度
- **21-89日**: 週次粒度（月曜日開始）
- **>=90日**: 月次粒度

これにより最適な可視化密度とパフォーマンスが保証されます。

## 4. コンポーネント定義

### コンポーネント1: エンゲージメントKPI
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
        - ビジュアル優先度ガイダンス:
          * "primary": 目立つように表示（例: カウントは32pxボールド、率は24pxボールド）
          * "tertiary": 補足情報として表示（例: 13px通常、"Total Opens: {value}"）
        - すべての率計算はユニークカウント（COUNT DISTINCT message_id）を使用して、膨張したメトリクスを避ける必要があります。

### コンポーネント2: 収益KPI
- component:
    - component_id: "kpi_summary_revenue"
    - component_type: "kpi_card_group"
    - title: "Revenue KPIs for {name} ({id})"
    - source_tables: ["revenue", "email_events"]
    - display_condition: "campaign_idでフィルタリングしている場合のみこのコンポーネントを表示。"
    - query_hints:
        - "ジャーニーの収益を取得するには、'revenue'と'email_events'テーブルを'campaign_id'でJOINする必要があります。"
    - metrics:
        - { metric_id: "total_revenue", display_name: "Total Revenue", calculation: "SUM(total_revenue) from revenue table where attribution_type is 'direct' or 'contributed'", format: "currency", display_condition: "直接収益と貢献収益の両方が存在する場合のみ表示。" }
        - { metric_id: "direct_revenue", display_name: "Direct Revenue", calculation: "SUM(total_revenue) from revenue table where attribution_type = 'direct'", format: "currency" }
        - { metric_id: "contributed_revenue", display_name: "Contributed Revenue", calculation: "SUM(total_revenue) from revenue table where attribution_type = 'contributed'", format: "currency" }

### コンポーネント3: メール件名別パフォーマンス
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
          1. email_eventsテーブルから直接email_titleでGROUP BY
          2. campaign_idまたはjourney_idでフィルタ
          3. event_masterテーブルとのJOINは不要
        - SQLエージェントはLIMIT 51でクエリする必要があります。
        - 51行が返された場合、VIZエージェントは注記を表示する必要があります: '上位50件のみ表示しています。追加の件名が表示されていない可能性があります。'
        - 最初の50行のみを表示します。

### コンポーネント4: エンゲージメント数トレンド
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
        - このコンポーネントは'event_timestamp'カラムに基づいています。
        - ゼロパディングは不要です。
        - 時間粒度はキャンペーン/ジャーニーデータの総日付範囲によって決定されます（セクション3参照）。
        - すべてのメトリクスは開封とクリックにCOUNT DISTINCT message_idを使用して、膨張したカウントを避けます。

### コンポーネント5: コンバージョン・収益トレンド
- component:
    - component_id: "conversions_trend"
    - component_type: "line_chart"
    - title: "Conversions & Revenue Trend"
    - source_tables: ["revenue", "email_events"]
    - y_axis_shared: false
    - visualization_hint: "mode: 'lines+markers', dual y-axis (left: count, right: currency)"
    - display_condition: "campaign_idでフィルタリングしている場合のみ表示。"
    - metrics:
        - { metric_id: "conversions", display_name: "Conversions", calculation: "COUNT(DISTINCT conversion_id) FROM revenue", format: "integer", y_axis: "left" }
        - { metric_id: "direct_revenue", display_name: "Direct Revenue", calculation: "SUM(total_revenue) FROM revenue WHERE attribution_type = 'direct'", format: "currency", y_axis: "right" }
        - { metric_id: "contributed_revenue", display_name: "Contributed Revenue", calculation: "SUM(total_revenue) FROM revenue WHERE attribution_type = 'contributed'", format: "currency", y_axis: "right" }
        - { metric_id: "total_revenue", display_name: "Total Revenue", calculation: "SUM(total_revenue) FROM revenue WHERE attribution_type IN ('direct', 'contributed')", format: "currency", y_axis: "right" }
    - notes: |
        - このコンポーネントは'conversion_timestamp'カラムに基づいています。
        - ゼロパディングは不要です。
        - 時間粒度はキャンペーン/ジャーニーデータの総日付範囲によって決定されます（セクション3参照）。
        - デュアルy軸を使用: カウントメトリクス（コンバージョン）は左、通貨メトリクス（収益）は右。
        - このコンポーネントは曜日パターンやキャンペーンタイミング効果の特定に役立ちます。

## 5. コンポーネントレンダリング順序

最終出力は以下の順序でコンポーネントをレンダリングする必要があります：

1. Title
2. Summary（データドリブンなインサイト）
3. kpi_summary_engagement
4. kpi_summary_revenue（campaign_idでデータが存在する場合）
5. engagement_count_trend
6. conversions_trend（campaign_idでデータが存在する場合）
7. email_title_performance
