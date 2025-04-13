# 📣 Treasure Data CDP: Activation Actions ワークフロー

このワークフローは、Treasure Data CDP の Activation Actions 機能を活用して、ハッシュ化されたメールアドレスをもとに、生のメールアドレスを結合する仕組みです。ハッシュ化された値をキーとして、別テーブルに格納された生のメールアドレスを安全に参照することで、外部チャネルへの配信準備を整えます。

## 🛠 設定項目

ワークフローを実行する前に、以下の設定値をプロジェクトに合わせて変更してください：

```yaml
_export:
  td:
    database: '${activation_actions_db}'  # 処理対象のデータベース名
  hashed_email_column: 'hashed_email'     # Activationテーブル内のハッシュ化されたメールアドレスのカラム名
  raw_email_db_table: 'support.profile_table'  # 生のメールアドレスが格納されたテーブル（例: database.table 形式）
  raw_email_column: 'email'               # 生のメールアドレスのカラム名
```

## ▶ Activation 処理

実際のアクティベーション処理は `+activation_for_added_profiles` タスクで実行され、`activation.sql` に記述されたSQLが使用されます。

### SQL 処理内容

```sql
SELECT t2.email, t1.* 
FROM 
  (SELECT * FROM ${activation_actions_table}) t1
LEFT JOIN
  (SELECT ${raw_email_column} AS email FROM ${raw_email_db_table}) t2
ON t1.hashed_email = TO_HEX(SHA256(TO_UTF8(email)))
```

- hashed_email カラムと、生メールアドレスに対して SHA-256 でハッシュ化した値をマッチさせる設計です。
- t2.email に結合された生のメールアドレスが出力されます。

### 補足：
- ハッシュ化されたメールと生のメールをSHA-256で照合することで、安全なマッチングを実現します。
- テスト完了後に必要に応じて以下の項目を有効化し、Engageへの結果出力を設定してください：
  ```yaml
  # result_connection: ${result_connection_name}
  # result_settings: ${result_connection_settings}
  ```


## ✅ 前提条件

- Activation テーブルには `SHA-256` でハッシュ化されたメールアドレス（Hex形式）が含まれている必要があります。
- 生のメールアドレスを格納したテーブルにアクセスできる必要があります。
- 使用するテーブル・データベースには適切な権限が付与されている必要があります。

## 📂 ファイル構成

下記をTreasure Workflowにて設定しておくこと

- `workflow.dig`：TDワークフロー定義ファイル
- `activation.sql`：アクティベーションに使用するSQLクエリ

## 🧭 Audience Studio での Activation 設定手順

Treasure Data Console（Audience Studio）で、このワークフローを使用するための設定方法は以下のとおりです。

1. セグメント作成

Audience Studio で新規セグメントを作成するか、既存セグメントを選択します。
Audienceには hashed_email が含まれていることを確認します（SHA-256 でエンコード済みのHex文字列）。
他のハッシュ化アルゴリズムの場合には、SQLの変更が必要になります。

2. Activation の画面で、Activation Actionsの設定

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/9189bd43329b5ee121b99facb8f2d53e.png)](https://treasure-data.gyazo.com/9189bd43329b5ee121b99facb8f2d53e)


3. Output Column Mappingにてhashed emailカラムを指定

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/98045d86b19bcc92a3a79ba1f8992bd6.png)](https://treasure-data.gyazo.com/98045d86b19bcc92a3a79ba1f8992bd6)

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/95102908c21edd9027ff34cb723bd739.png)](https://treasure-data.gyazo.com/95102908c21edd9027ff34cb723bd739)

## 参考

- [Activation Actions Doc](https://docs.treasuredata.com/articles/#!pd/activation-actions)