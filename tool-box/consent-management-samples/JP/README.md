# オプトアウト/オプトインと同意管理に関するサンプル集

Treasure Dataの計測SDKである[TD-JS-SDK](https://github.com/treasure-data/td-js-sdk)を利用する上で必要となる、デバイス識別ならびにデータ利用に関する同意管理についてのサンプルコードです。
これらのサンプルコードは現状渡しであり、あくまでサンプルであることをご理解ください。個々の処理内容や同意取得に関する文章については、各企業のプライバシーポリシーや法務部門あるいは顧問弁護士の方の助言に従ってください。

## TD-JS-SDKに組み込まれているオプトアウト機能

TD-JS-SDK 2.x には2つのオプトアウト機能が内蔵されています。（1.xには含まれませんのでご注意ください）
実装例は [consent-builtin.html](./consent-builtin.html) をご覧下さい。

### Anonymous Mode と Signed Mode

- Anonymous Mode はデバイスを一意に識別する情報を記録しません。例えばJavaScriptと1st party cookieで管理している `td_client_id` や、IPアドレス `td_ip` は記録されず、匿名情報のみが記録されます。
- Signed Mode では、デバイスを一意に識別する `td_client_id`, `td_global_id` そして `td_ip` 等が記録されます。

SDKのデフォルトは Anonymous Mode ですが、一般的な実装としては `startInSignedMode` オプションまたは `setSignedMode()` メソッドにより Signed Modeで利用されていることがあります。

- Anonymous ModeからSigned Modeへの切り替えは `td.setSignedMode()` を呼ぶことで行えます。
- Signed ModeからAnonymous Modeへの切り替えは `td.setAnonymousMode()` を呼ぶことで行えます。

実装例の中では、「オプトアウト（匿名化する）」がクリックされた場合に Anonymous Mode へ、「オプトイン（識別に同意する）」がクリックされた場合に Signed Mode へ切り替えています。

### blockEvents と unblockEvents

- blockEvents はデータ送信を停止します。
- unblockEvents は停止していたデータ送信を再開します。

SDKのデフォルトでは unblockEvents 相当の状態、つまりデータ送信が行われる状態です。

- データ送信を止める場合、 `td.blockEvents()` を呼びます。
- データ送信を再開する場合、 `td.unblockEvents()` を呼びます。

## より高度な同意管理の例

### 告知とオプトアウトページへの動線

こちらの実装例 [consent-overlay.html](./consent-overlay.html) では、画面右下にオーバーレイする形で告知ダイアログを表示しています。
「閉じる」ボタンがクリックされるとダイアログは消え、以降はダイアログは表示されません。（この状態管理にCookieを利用しています）

あくまで計測に関する告知とオプトアウトを希望する場合の案内のみで、このダイアログ自体では同意管理を行いません。
この実装例はタグマネジメントツール等から配信できるよう、1つの `script` タグで完結しています。

### SDKそのもののロードを停止する

より厳しいオプトアウト方式として、SDKそのものをロードしない方法が必要な場合はこちらの実装例 [consent-full.html](./consent-full.html) をご参照ください。
TD-JS-SDKに組み込まれたオプトアウト機能を用いず、SDKの外側で制御を行っています。

SDKに組み込まれたオプトアウト機能を利用する場合、最低でもTD-JS-SDK自体をロードする必要がありますが、この実装例ではTreasure Dataに対するいかなる通信も発生しません。
こちらの実装例もタグマネジメントツール等からの配信に対応しています。

### GDPRやCCPAへの適合を視野に入れる方式

単にオプトアウトを提供するだけではなく、データの利用目的に応じた同意管理を行う実装例がこちら [consent-detailed.html](./consent-detailed.html) です。
詳細は実装例のHTML中に記載されています。

この方法では、「一意なデバイスを識別するための情報を扱うか否か」と3つの利用目的として「サービス改善のためのデータ分析」「パーソナライズ等へのデータ利用」「広告目的にサービスの外部でのデータ利用」に対してそれぞれ同意管理を行います。
こちらもタグマネジメントツール等からの配信に対応している他、Treasure Data以外のツールについても制御することを想定した実装例となっています。