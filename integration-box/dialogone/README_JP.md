# Integration of DialogOne with Treasure Data 
DACが開発・提供している「DialogOne」は、コミュニケーションプラットフォームであるLINEと連携した、メッセージング管理ソリューションです。
企業が保有するCDP（カスタマー・データ・プラットフォーム）などの自社データベースとシームレスに連携し、LINE公式アカウントをマーケティングに活用することが可能となります。
そして、このWorkflowを使ってセグメントユーザーのリストをDialogOneに送信します。

# 事前に必要なもの
- 次のパラメータは必須です。

| 変数 | 備考 | データ例 | データ取得元 |
| -------- | ----------- | -------- | -------- |
| acid |アカウント識別子 | `abcdef123456789a`| DAC |
| sa_email | サービスアカウントのE-mailアドレス | `example@test-project.iam.gserviceaccount.com`| DAC |
| private_key | サービスアカウントの秘密鍵 | `-----BEGIN PRIVATE KEY-----\nABCDEFGHIJKLMNOPQRSTUVWXYZ......abcdefghijklmnopqrstuvwxyz+1234567890=\n-----END PRIVATE KEY-----\n`| DAC |
| private_key_id | サービスアカウントの秘密鍵ID | `abcdef123456789abcdef123456789abcdef1234`| DAC |
| td.apikey | **Master**のAPIキー([link](https://docs.treasuredata.com/display/public/PD/Getting+Your+API+Keys)) | `1234/abcdefghijklmnopqrstuvwxyz1234567890`| Treasure Data |
| database | ユーザーIDを格納するテーブルが存在するデータベース名 | `sample_database` | Treasure Data |
| filename | 出力するCSVファイルにつけるファイル名 (※255文字以下で半角英数字、アンダーバー、ドット、ハイフンのみ使用可能) | `output_user_list`|  |
| sqlfile | ユーザーIDリストを取得するためのクエリが記載されているファイル名 | `user_id_list.sql` |  |

# SQLクエリ
下記のようにLINE userID用のカラムのみ取得するクエリを作成してください。

`user_id_list.sql`
```
SELECT 
  user_id
FROM
  sample_db.sample_table
```

# インストール (TD Toolbelt)  
### 1. アップロードするファイルを用意する
Githubからファイルをダウンロード・解凍が完了したら、解凍したディレクトリ内にユーザーID取得用のクエリが記載されたSQLファイルを置いてください。

Digdagファイル(.dig)の方をエディタで開き、 `td.apikey`、`private_key`、`private_key_id`**以外**の変数の値を用意したものに書き換えてください。

なお、Digdagファイルは任意のプロジェクト名で変更可能ですが、Pythonファイル(.py)の方の名前は変更しないでください。



### 2. Treasure Dataにアップロードする
Digdagファイルを同じディレクトリに移動し、下記のコマンドを実行してください。


    $ td wf push [Digdag file name]
### 3. Secretを設定する
[Secrets](https://docs.treasuredata.com/display/public/PD/About+Workflow+Secret+Management)の値を設定してください。
`private_key`は値が長いのでテキストファイルに保存して下記のようにアップロードをする事をおすすめします。  (そのテキストファイルはアップロードしないように！)

    $ td wf secrets --project [Digdag file name] --set td.apikey
    $ td wf secrets --project [Digdag file name] --set private_key=@private_key.txt
    $ td wf secrets --project [Digdag file name] --set private_key_id


# その他参考
- TD Toolbelt
https://docs.treasuredata.com/display/public/PD/Treasure+Workflow+Quick+Start+using+TD+Toolbelt+in+a+CLI
- pytd
https://github.com/treasure-data/pytd
