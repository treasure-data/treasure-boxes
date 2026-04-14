# Report Specification: OverallSummary（日本語版）

> **注意**: このドキュメントは参考資料です。正式なレポート仕様は英語版（[OverallSummary_Spec.md](./OverallSummary_Spec.md)）を参照してください。

## 1. レポート概要
- purpose: "指定された期間における主要パフォーマンス指標（KPI）、トレンド、上位キャンペーン/ジャーニーを可視化する。"
- source_tables:
    - "daily_summary"
    - "events_master" # ランキングでの名前検索に使用

## 2. フィルタ
- filter:
    - id: "date_range"
    - type: "date"
    - required: true
    - notes: |
        - 日付範囲（start_date, end_date）は必須です。
        - 範囲が指定されない場合、SQLエージェントは利用可能な最小/最大日付とエラーを返してください。
        - SQLエージェントは範囲を検証します。365日を超える場合、リクエストを拒否し、有効な365日範囲を提案するメッセージを返します。

## 3. メトリクスに関する重要な注意事項

**注意:** このセクションは計算方法論を説明します。レポートの最後にユーザー向け免責事項を表示する必要があります（Component: data_methodology_disclaimerを参照）。

## 4. コンポーネント定義
- component:
    - component_id: "kpi_summary"
    - component_type: "kpi_card_group"
    - title: "Overall Performance Summary"
    - metrics:
        - { metric_id: "sends", display_name: "Sends", calculation: "SUM(total_sends)", format: "integer" }
        - { metric_id: "total_revenue", display_name: "Total Revenue", calculation: "SUM(total_revenue_direct + total_revenue_contributed)", format: "currency", display_condition: "SUM(total_revenue_direct) > 0 AND SUM(total_revenue_contributed) > 0の場合のみ表示" }
        - { metric_id: "direct_revenue", display_name: "Direct Revenue", calculation: "SUM(total_revenue_direct)", format: "currency" }
        - { metric_id: "contributed_revenue", display_name: "Contributed Revenue", calculation: "SUM(total_revenue_contributed)", format: "currency" }
        - { metric_id: "conversions", display_name: "Conversions", calculation: "SUM(total_conversions)", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "SUM(total_deliveries)", format: "integer" }
        - { metric_id: "opens", display_name: "Opens", calculation: "SUM(total_opens)", format: "integer" }
        - { metric_id: "open_rate", display_name: "Open Rate", calculation: "SUM(total_opens) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "clicks", display_name: "Clicks", calculation: "SUM(total_clicks)", format: "integer" }
        - { metric_id: "click_rate", display_name: "Click Rate", calculation: "SUM(total_clicks) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "bounces", display_name: "Bounces", calculation: "SUM(total_hard_bounces + total_soft_bounces)", format: "integer" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "SUM(total_hard_bounces + total_soft_bounces) / SUM(total_sends)", format: "percentage" }
        - { metric_id: "unsubscribes", display_name: "Unsubscribes", calculation: "SUM(total_unsubscribes)", format: "integer" }

- component:
    - component_id: "campaign_performance_ranking"
    - component_type: "table"
    - title: "Top 5 Campaigns"
    - source_tables: ["daily_summary", "events_master"]
    - dimensions:
        - { id: "campaign_name", display_name: "Campaign Name" }
        - { id: "campaign_id", display_name: "Campaign ID" }
    - metrics:
        - { metric_id: "revenue", display_name: "Revenue", format: "currency" }
        - { metric_id: "conversions", display_name: "Conversions", calculation: "SUM(total_conversions)", format: "integer" }
        - { metric_id: "sends", display_name: "Sends", calculation: "SUM(total_sends)", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "SUM(total_deliveries)", format: "integer" }
        - { metric_id: "open_rate", display_name: "Open Rate", calculation: "SUM(total_opens) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "click_rate", display_name: "Click Rate", calculation: "SUM(total_clicks) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "SUM(total_hard_bounces + total_soft_bounces) / SUM(total_sends)", format: "percentage" }
    - orderby_clause_template: "ORDER BY SUM(total_revenue_direct + total_revenue_contributed) DESC, SUM(total_conversions) DESC, SUM(total_clicks) DESC, campaign_id DESC"
    - notes: |
        - このコンポーネントはキャンペーンをランク付けします。最終ソート順は提供された'orderby_clause_template'を使用する必要があります。
        - 日付フィルタリングは'summary_date'カラム（varchar）を使用し、文字列ベースの比較を行う必要があります（例: WHERE summary_date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'）。
        - 表示する'Revenue'カラムは動的です。エージェントは以前に議論したルールに基づいてTotal、Direct、またはContributed Revenueを表示するCASE文を構築する必要があります。

- component:
    - component_id: "journey_performance_ranking"
    - component_type: "table"
    - title: "Top 5 Journeys"
    - source_tables: ["daily_summary", "events_master"]
    - dimensions:
        - { id: "journey_name", display_name: "Journey Name" }
        - { id: "journey_id", display_name: "Journey ID" }
    - metrics:
        - { metric_id: "revenue", display_name: "Revenue", format: "currency" }
        - { metric_id: "conversions", display_name: "Conversions", calculation: "SUM(total_conversions)", format: "integer" }
        - { metric_id: "sends", display_name: "Sends", calculation: "SUM(total_sends)", format: "integer" }
        - { metric_id: "deliveries", display_name: "Deliveries", calculation: "SUM(total_deliveries)", format: "integer" }
        - { metric_id: "open_rate", display_name: "Open Rate", calculation: "SUM(total_opens) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "click_rate", display_name: "Click Rate", calculation: "SUM(total_clicks) / SUM(total_deliveries)", format: "percentage" }
        - { metric_id: "bounce_rate", display_name: "Bounce Rate", calculation: "SUM(total_hard_bounces + total_soft_bounces) / SUM(total_sends)", format: "percentage" }
    - orderby_clause_template: "ORDER BY SUM(total_revenue_direct + total_revenue_contributed) DESC, SUM(total_conversions) DESC, SUM(total_clicks) DESC, journey_id DESC"
    - notes: |
        - このコンポーネントはジャーニーをランク付けします。最終ソート順は提供された'orderby_clause_template'を使用する必要があります。
        - 日付フィルタリングは'summary_date'カラム（varchar）を使用し、文字列ベースの比較を行う必要があります。
        - 表示する'Revenue'カラムは動的です。

- component:
    - component_id: "performance_trend"
    - component_type: "trend_chart"
    - title: "Performance Trend"
    - tabs:
        - tab_name: "Engagement"
          metrics:
            - { metric_id: "sends", display_name: "Sends", calculation: "SUM(total_sends)" }
            - { metric_id: "deliveries", display_name: "Deliveries", calculation: "SUM(total_deliveries)" }
            - { metric_id: "clicks", display_name: "Clicks", calculation: "SUM(total_clicks)" }
        - tab_name: "Revenue"
          metrics:
            - { metric_id: "revenue", display_name: "Revenue", calculation: "SUM(total_revenue_direct + total_revenue_contributed)" }
          display_condition: "期間の総収益 > 0の場合のみタブを表示"
    - notes: |
        - このコンポーネントは'summary_date'（varchar）カラムを使用します。date_truncなどの日付関数にはCAST(summary_date AS DATE)を使用する必要があります。
        - SQLエージェントは日付範囲の長さに基づいて時間粒度を動的に設定する必要があります：
          * <=20日: 日次
          * 21-89日: 週次（月曜日開始）
          * >=90日: 月次
        - エージェントは連続した時系列を確保するためにゼロパディングを実行する必要があります。

- component:
    - component_id: "data_methodology_disclaimer"
    - component_type: "text_note"
    - title: "Data Aggregation Methodology"
    - content: |
        注意: このレポートの開封率とクリック率は、daily_summaryテーブルの総イベントカウントに基づいて計算されています。
        同じメールが複数回開封またはクリックされた場合、各イベントは個別にカウントされます。
        これにより、ユニーク開封/クリック率よりも高い率が表示される場合があります。

        ユニークカウントベースのメトリクスによる詳細な分析については、Campaign Detailsレポートを参照してください。
    - display_condition: "ALWAYS - このコンポーネントはすべてのレポートの最後に必ず表示する必要があります。"
    - notes: |
        - 重要: この免責事項は常にレポートの最後、他のすべてのコンポーネントの後にレンダリングされる必要があります。
        - これはオプションではありません - データやフィルタに関わらず、すべてのOverallSummaryレポートに表示される必要があります。
        - レンダリングスタイル: プレーンテキストのみ、ボーダーなし、背景色なし、ボックスシャドウなし、ボールドテキストなし。
        - 通常のフォントウェイト（ボールドでない）、通常のフォントサイズ（14-16px）を使用。
        - 背景色: transparentまたはページ背景と同じ（白/ライトグレー）。
        - 視覚的なハイライトや強調なし - シンプルなフッターテキストとしてページに溶け込むべきです。

## 5. コンポーネントレンダリング順序

最終出力は以下の順序でコンポーネントをレンダリングする必要があります：

1. Report Title
2. Summary（データドリブンなインサイト）
3. kpi_summary
4. campaign_performance_ranking
5. journey_performance_ranking
6. performance_trend
7. **data_methodology_disclaimer** ← 必ず最後

**重要:** data_methodology_disclaimerコンポーネントは、他のコンポーネントのレンダリングやデータの可用性に関わらず、常にレポートの最後に表示される必要があります。
