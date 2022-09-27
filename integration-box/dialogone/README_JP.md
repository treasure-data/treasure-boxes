# Integration of DialogOne with Treasure Data 
DACが開発・提供している「DialogOne」は、コミュニケーションプラットフォームであるLINEと連携した、メッセージング管理ソリューションです。
企業が保有するCDP（カスタマー・データ・プラットフォーム）などの自社データベースとシームレスに連携し、LINE公式アカウントをマーケティングに活用することが可能となります。
そして、このWorkflowを使ってセグメントユーザーのリストをDialogOneに送信します。

# 事前に必要なもの
- 次のパラメータは必須です。

| 変数 | 備考 | データ例 | データ取得元 |
| -------- | ----------- | -------- | -------- |
| acid |アカウント識別子 | `abcdef123456789a`| DAC |
| api_key | APIキー | `a1b2c3d4-5ef6-777a-888b-9abc12ed345f`| DAC |
| service_id | サービスID | `4`| DAC |
| td.apikey | **Master**のAPIキー([link](https://docs.treasuredata.com/display/public/PD/Getting+Your+API+Keys)) | `1234/abcdefghijklmnopqrstuvwxyz1234567890`| Treasure Data |
| database | ユーザーIDを格納するテーブルが存在するデータベース名 | `sample_database` | Treasure Data |
| table | ユーザーIDを格納するテーブル | `sample_table` | Treasure Data |
| user_id_column | ユーザーIDを格納されているカラム名 | `user_id` | Treasure Data |

# アップロードファイルについて
以前アップロードしたものと同じ名前でファイルをアップロードした場合、後から登録したもので上書きされます。  
また、登録したファイルの有効期限は30日で、登録/更新後30日を超過したファイルは削除されます。

# インストール (TD Toolbelt)  
### 1. アップロードするファイルを用意する
Githubからファイルをダウンロード・解凍が完了したら、Treasure Data環境にアップロードします。

Digdagファイル(.dig)の方をエディタで開き、`_export`部分の変数の値を用意したものに書き換えてください。

なお、Digdagファイルは任意のプロジェクト名で変更可能ですが、Pythonファイル(.py)の方の名前は変更しないでください。


### 2. Treasure Dataにアップロードする
Digdagファイルを同じディレクトリに移動し、下記のコマンドを実行してください。


    $ td wf push [Digdag file name]
### 3. Secretを設定する
- td.apikey
- api_key (provided by DAC)
- acid (provided by DAC)
- service_id (provided by DAC)

これらの値を[Secrets](https://docs.treasuredata.com/display/public/PD/About+Workflow+Secret+Management)として設定してください。

    $ td wf secrets --project [Digdag file name] --set td.apikey
    $ td wf secrets --project [Digdag file name] --set api_key
    $ td wf secrets --project [Digdag file name] --set acid
    $ td wf secrets --project [Digdag file name] --set service_id

# その他参考
- TD Toolbelt
https://docs.treasuredata.com/display/public/PD/Treasure+Workflow+Quick+Start+using+TD+Toolbelt+in+a+CLI
- pytd
https://github.com/treasure-data/pytd
