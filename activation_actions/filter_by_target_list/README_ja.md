# Activation Actions: ターゲットリストによるParent Segmentフィルタリング

このサンプルは、Treasure Data の Activation Actions で匿名IDを使用してターゲットリストテーブルとJOINし、Parent Segmentをフィルタリングする方法を示します。

公式サンプル: https://github.com/treasure-data/treasure-boxes/tree/master/activation_actions

## 目的

1. **Activation Actions の使用**: String Builder で指定したテーブル名をカスタムパラメータとして受け取る
2. **Parent Segment の構造**: email と匿名ID (anonymous_id) のフィールドを持つ
3. **動的なテーブル JOIN**: 指定されたターゲットテーブルと Parent Segment を匿名IDでJOINし、ターゲットリストに存在するレコードのみをフィルタリング
4. **最終出力**: フィルタ結果を Engage Studio でのメール配信に使用可能な形式で出力

## ファイル構成

```
.
├── filter_by_target_list.dig    # メインワークフロー定義
├── queries/
│   ├── filter_segment.sql          # フィルタリングクエリ
│   ├── setup_sample_data.sql       # サンプルデータ参照
│   ├── setup_parent_segment.sql    # Parent Segmentテーブル作成
│   └── setup_target_list.sql       # ターゲットリストテーブル作成
├── images/
│   ├── activation_actions_config.png  # Output Mapping設定画面
│   ├── parent_segment_data.png        # ターゲットリストのデータ
│   ├── query_result.png               # フィルタ結果
│   ├── workflow_execution.png         # Target Audience設定画面
│   └── workflow_result.png            # ワークフロー設定画面
├── README.md                        # 英語版ドキュメント
└── README_ja.md                     # このファイル（日本語版ドキュメント）
```

## データ構造

### Parent Segment テーブル
```sql
parent_segment (
  anonymous_id VARCHAR,   -- 匿名ID (JOIN KEY)
  email VARCHAR,          -- メールアドレス
  created_at BIGINT,      -- 作成日時
  updated_at BIGINT       -- 更新日時
)
```

### ターゲットリストテーブル (例: campaign_target_list)
```sql
campaign_target_list (
  anonymous_id VARCHAR,   -- 匿名ID (JOIN KEY)
  campaign_id VARCHAR     -- キャンペーンID
)
```

### 出力
```sql
-- Parent Segmentの全カラム
-- (ターゲットテーブルに存在するレコードのみ)
anonymous_id VARCHAR,
email VARCHAR,
created_at BIGINT,
updated_at BIGINT,
...
```

## Activation Actionsのビルトインパラメータ

Activation Actions では以下のパラメータが自動的に渡されます:

- `activation_actions_db`: Parent Segment が格納されているデータベース名
- `activation_actions_table`: Parent Segment のテーブル名（完全修飾名: `database.table`）

詳細: https://docs.treasuredata.com/articles/#!pd/activation-actions-parameters

## ワークフローの動作

### 1. パラメータ受け取り

このワークフローは以下のパラメータを使用します:

- `activation_actions_db`: Activation Actionsから自動的に渡されるデータベース名
- `activation_actions_table`: Activation Actionsから自動的に渡されるParent Segmentテーブル名（完全修飾名: `database.table`）
- `integration_db`: ターゲットテーブルが格納されているデータベース名（カスタムパラメータ、デフォルト: `integration_db`）
- `target_table_name`: String Builder で指定するターゲットテーブル名（カスタムパラメータ）

### 2. フィルタリング処理

`queries/filter_segment.sql` が実行され:

1. `${activation_actions_table}` (Parent Segment - データベース名を含む) を読み込む
2. 指定されたターゲットテーブル (`${integration_db}.${target_table_name}`) と匿名ID で INNER JOIN
3. email と anonymous_id が NULL でないレコードのみを抽出
4. Parent Segmentの全カラムを返す（ターゲットテーブルのカラムは含まない）
5. 結果を Activation の出力として返す（または `result_connection` で指定した宛先に送信）

### 3. 出力

- デフォルト: クエリ結果が Activation の出力として返される
- オプション: `result_connection` と `result_settings` を指定することで、Engage Studio などに直接エクスポート可能

## 実行方法

### Activation Actions での設定

1. **Segment Builder** で Parent Segment を作成
   - anonymous_id と email フィールドを含むこと

2. **Activation Actions** で以下を設定:
   - Action Type: Treasure Workflow
   - Workflow project name: `filter_by_target_list`
   - Workflow name: `filter_by_target_list`
   - Custom Parameters (String Builder):
     ```
     integration_db=integration_db
     target_table_name=campaign_target_list
     ```

   ![Activation Actions設定画面](images/workflow_result.png)

### ワークフローのアップロード

```bash
# ワークフローをTreasure Dataにアップロード
td wf push filter_by_target_list
```

### ローカルでのテスト実行

```bash
# Activation Actionsの環境をシミュレートしてテスト
td wf run filter_by_target_list.dig \
  -p activation_actions_db=sample_db \
  -p activation_actions_table=sample_db.parent_segment \
  -p integration_db=integration_db \
  -p target_table_name=campaign_target_list
```

## データフロー図

```
┌─────────────────────────┐
│   Parent Segment        │
│  (email, anonymous_id)  │
└───────────┬─────────────┘
            │
            │ INNER JOIN (anonymous_id)
            │
┌───────────▼─────────────┐
│   Target Table          │
│  (anonymous_id, ...)    │
└───────────┬─────────────┘
            │
            │ Filter
            │
┌───────────▼─────────────┐
│ Filtered Result         │
│ (All Parent Segment     │
│  columns)               │
└─────────────────────────┘
            │
            ▼
   Engage Studio (Email)
```

## サンプルデータでの動作例

### 1. Target Audience の設定

emailと匿名IDフィールドを含むParent Segmentを選択します。

![Target Audience](images/workflow_execution.png)

### 2. Output Mapping の設定

出力カラムとString Builderパラメータを設定します:
- **Attribute Columns**: セグメントからemailフィールドをマッピング
- **String Builder**: `target_table_name` パラメータを設定（例: `campaign_target_list`）

![Output Mapping](images/activation_actions_config.png)

### 3. ターゲットリストのデータ

ターゲットテーブル（`integration_db.campaign_target_list`）には3件のレコードのみが含まれています:

![Target List](images/parent_segment_data.png)

### 4. フィルタ結果

ワークフロー実行後、ターゲットリストに一致する3件のレコードのみが返されます:

![Query Result](images/query_result.png)

**要約:**
- Parent Segment: 5件（anon_001 から anon_005）
- Target List: 3件（anon_001, anon_003, anon_005）
- フィルタ結果: Parent Segmentの全カラムを含む3件

## 次のステップ

このサンプルではActivation Actionsを使用したコアフィルタリングロジックを実装しています。
実際の運用では、以下を追加実装することを検討してください:

1. **Engage Studio へのエクスポート**

   `filter_by_target_list.dig` の `result_connection` と `result_settings` パラメータのコメントを外します:
   ```yaml
   +filter_by_target_list:
     td>: queries/filter_segment.sql
     result_connection: ${result_connection_name}
     result_settings: ${result_connection_settings}
   ```

2. **エラーハンドリング**
   - ターゲットテーブルが存在しない場合の処理
   - JOIN 結果が0件の場合の通知

3. **ログ記録**
   - フィルタ前後のレコード数
   - 実行ログのトラッキング

## 注意事項

- `target_table_name` は必須パラメータです
- `integration_db` パラメータでターゲットテーブルが格納されているデータベースを指定します（Parent Segmentとは別のデータベースでも可）
- `activation_actions_table` は完全修飾テーブル名（データベース名を含む）なので、直接使用します
- anonymous_id は両方のテーブルで NULL でない値を持つ必要があります
- INNER JOIN を使用しているため、Target Table に存在しないレコードは除外されます
- 結果にはParent Segmentの全カラムのみが含まれます（ターゲットテーブルのカラムは含まれません）
