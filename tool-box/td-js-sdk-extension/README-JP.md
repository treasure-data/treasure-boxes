# Extension for Treasure Data's TD-JS-SDK

[English document available here / 英語のドキュメントはこちら](README.md)

**注意： このライブラリは Treasure Data 社の製品ではないことをご留意ください。自己責任でご利用ください。**

## 導入

まず先に、 `/example/index.html` を見てください。導入方法について理解するのに役立ちます。

1. TD-JS-SDKローダーをhtmlに埋め込みます。これは [公式の TD-JS-SDK 実装](https://github.com/treasure-data/td-js-sdk#installing) と同じ手順です。
**この最初のステップ以外の手順は行わないでください。 `new Treasure()` や他のコードは必要ありません。全て `config.js` に内用されています。**

```html
<!-- Treasure Data -->
<script type="text/javascript">
!function(t,e){if(void 0===e[t]){e[t]=function(){e[t].clients.push(this),this._init=[Array.prototype.slice.call(arguments)]},e[t].clients=[];for(var r=function(t){return function(){return this["_"+t]=this["_"+t]||[],this["_"+t].push(Array.prototype.slice.call(arguments)),this}},s=["blockEvents","setSignedMode","fetchServerCookie","unblockEvents","setSignedMode","setAnonymousMode","resetUUID","addRecord","fetchGlobalID","set","trackEvent","trackPageview","trackClicks","ready"],n=0;n<s.length;n++){var o=s[n];e[t].prototype[o]=r(o)}var c=document.createElement("script");c.type="text/javascript",c.async=!0,c.src=("https:"===document.location.protocol?"https:":"http:")+"//cdn.treasuredata.com/sdk/2.2/td.min.js";var i=document.getElementsByTagName("script")[0];i.parentNode.insertBefore(c,i)}}("Treasure",this);
</script>
```

2. `/dist` ディレクトリ内の2つのファイルを埋め込んでください。1つはこの拡張のコアファイル、もう一つは設定と初期化のファイルです。
  - `td-js-sdk-ext.js` はこの拡張のコアライブラリです
  - `config.js` は計測に必要な全てを内包しています

```html
<script src="td-js-sdk-ext.js"></script>
<script src="config.js"></script>
```

3. `config.js` を以下の「構成」セクションの手順に従って変更します。


## 構成

### TreasureData 標準の設定変数

`config.js` の冒頭に、 TD-JS-SDKを初期化するための `var td = new Treasure({...});` のような行があります。
これはTD-JS-SDKの標準的な設定プロセスなので、 [TD-JS-SDK Readme 中の公式リファレンス](https://github.com/treasure-data/td-js-sdk#treasureconfig) を参照しながら各変数をセットしてください。

### Extension 固有の設定変数

`new Treasure({...})` の数行後に、`tdext.init({...})` のようなもう一つの初期化メソッド呼び出しがあります。
何を計測するか、イベントの粒度をどうするかを制御可能です。

|変数|例|説明|
|:---|:---|:---|
|`table`|`weblog`|拡張によって計測された全てのデータを格納するテーブル名|
|`eventName`|`TDExtRecurringEvent`|拡張は可視性の監視のために再帰イベントを発火します。 必要があればイベント名を変更します|
|`eventFrequency`|`250`|再帰イベントを間引く間隔です。これは計測精度とユーザー体験に直結しています|
|`targetWindow`|`self`|観測対象のフレームを指定しますが、TD-JS-SDKがiframe内での動作に適さないため、基本的に `self` であるべきです|
|`tdNs`|`td`|TD-JS-SDK のオブジェクトの名前空間|

### セッションIDサポート

- 少なくないウェブアナリストがまだ「セッション」に基づく行動の集計をしており、もしレコードにセッションIDが無ければSQLで対処することになります。
- このSDKは、 `options.session.enable` に `true` をセットすることで、セッションIDをセット・計測することができます。また、以下の追加オプションが利用できます：

|変数|例|説明|
|:---|:---|:---|
|domain|`example.com`|Cookie発行元ドメイン。もしサブドメインを跨いでCookieを共有したい場合、親ドメインを指定します|
|lifetime|`1800`|Cookieの有効期限の秒。もし訪問者がこの指定秒数以上ビーコンを送らないでいた場合、セッションは次のページで更新されます|

- この機能は `tdextSesId` という名前のCookieを1つ利用します

### ページ上での滞在時間 (アンロード)

- アンロード計測はページがアンロードされる際に利用可能なイベントの一つにイベントリスナーをセットします
- ユーザーが特定のページビューの間に割いた正確な時間が得られます
- `tdext.init()` の中で、 `options.unlaod.enable` に対して `true` を設定します

### クリック計測

- クリック計測はクリックされた要素（またはその親要素）が、指定した `data-*` 属性を持っている場合に発動します
- `options.clicks.enable` に `true` がセットされていながら、 `options.clicks.targetAttr` を省略した場合、クリック計測は `data-*` 属性のない要素に対するクリックを計測します
- `tdext.init()` の中で、 `options.clicks.enable` に対して `true` を設定し、設定値を調整します：

|変数|例|説明|
|:---|:---|:---|
|`targetAttr`|`data-trackable`|対象となる要素を特定するための属性名|

- もし `targetAttr` に `data-trackable` がセットされている場合、計測したい全ての要素に `data-trackable` 属性を追加する必要があります
- 理想的には、全てのブロック要素が階層のように構造化されていて、それぞれのブロック要素が `data-trackable` に意味のある値を持っているべきです

### スクロール深度

- 高さ固定のページと無限スクロール（遅延読み込み）に対応するスクロール深度計測
- `tdext.init()` の中で、 `options.scroll.enable` に対して `true` を設定し、設定値を調整します：

|変数|例|説明|
|:---|:---|:---|
|`threshold`|`2`|ユーザーが Xパーセント/ピクセル 地点で、ここで指定した T秒以上とどまった場合、スクロール深度が計測されます|
|`granularity`|`20`|ここで指定した Xパーセント/ピクセル 深度が増加するごとに計測されます|
|`unit`|`percent`|高さ固定のページの場合、`percent` が使えます。ページが無限スクロールの場合、代わりに `pixels` を指定します|

### 読了率

- 読了率はユーザーによってコンテンツのどれくらいの範囲が消費されたかを表す指標です
- `tdext.init()` の中で、 `options.read.enable` に対して `true` を設定し、設定値を調整します：

|変数|例|説明|
|:---|:---|:---|
|`threshold`|`4`|ユーザーが読了率X以上を、何秒以上維持したら計測するかの閾値です|
|`granularity`|`10`|ここで指定した割合で読了率が変化する度に計測されます|
|`target`|`document.getElementsById('article')`|記事本文（コンテンツ）を持つエレメント。読了計測の観測対象となるブロック要素を指定します|

### メディア計測

- このオプションを有効にすると、VIDEOまたはAUDIOの全てのメディアが自動計測されます
- このオプションは、 `play`, `pause` そして `eneded` イベントに加え、ハードビートをサポートします
- `tdext.init()` の中で、 `options.media.enable` に対して `true` を設定し、設定値を調整します：

|変数|例|説明|
|:---|:---|:---|
|`heartbeat`|`5`|ここで指定した X秒 ごとにハートビート計測が発動します|

### フォーム分析

- Form Analysisはフォームの完了についての統計情報を提供します。フォームのフィールドに入力された値は含みません
- この機能は、フォームo要素のリストを渡すことで、複数のフォームに対応します
- `tdext.init()` の中で、 `options.form.enable` に対して `true` を設定し、設定値を調整します：

|変数|例|説明|
|:---|:---|:---|
|`targets`|`document.getElementsByTagName('form')`|フォーム要素のリストを渡します|


## メソッド

### tdext.trackPageview(context, successCallback, failureCallback)

- ページビューイベントを計測
- いずれの引数も任意です

|引数|例|説明|
|:---|:---|:---|
|`context`|`{name: "hoge"}`|イベントに対する任意のコンテキストのオブジェクト|
|`successCallback`|`function(){}`|データ送信に成功した直後に実行させたい処理の関数名、または関数|
|`failureCallback`|`function(){}`|データ送信に失敗した直後に実行させたい処理の関数名、または関数|

### tdext.trackAction(action, category, context, successCallback, failureCallback)

- カスタムイベントを計測
- いずれの引数も任意ですが、 `action` と `category` は指定することを強く推奨します

|引数|例|説明|
|:---|:---|:---|
|`action`|`toggle`|アクション名|
|`category`|`switch`|アクションの対象|
|`context`|`{name: "hoge"}`|イベントに対する任意のコンテキストのオブジェクト|
|`successCallback`|`function(){}`|データ送信に成功した直後に実行させたい処理の関数名、または関数|
|`failureCallback`|`function(){}`|データ送信に失敗した直後に実行させたい処理の関数名、または関数|

### tdext.trackRead(target)

- 読了計測を初期化します
- もしページが遅延読込を使っている（無限スクロールで必要に応じてコンテンツを追記している）場合、新たに追加された記事を計測するため `trackRead()` によって再初期化すべきです。

|引数|例|説明|
|:---|:---|:---|
|`target`|`document.getElementById('article')`|記事本文（コンテンツ）を含むブロック要素|


## Action と Category の組み合わせ

|Action|Category|説明|
|:----|:----|:----|
|`view`|`page`|Pageview Event. One record per a pageview.|
|`rum`|`page`|A record for logging the performance information for Real User Monitoring. One record per a pageview.|
|`scroll`|`page`|A record with scroll depth data. Multiple records per a pageview.|
|`unload`|`page`|When the page is unloaded, this event will be transmitted. But Safari on iOS is not sending due to its limitation.|
|`read`|`content`|Records for Read-Through rate measurement. Multiple records per a pageview.|
|`click`|`link`|Click Tracking for `A` tags.|
|`click`|`button`|Click Tracking for other than `A` tags.|
|`play`|`video` or `audio`|When user start playing a video, this record will be created.|
|`pause`|`video` or `audio`||
|`timeupdate`|`video` or `audio`|Heartbeat data for media tracking.|
|`ended`|`video` or `audio`||
|`stats`|`form`|A record for Form Analysis. The data is sent on `unload` event.|
|`answer`|`survey`|If you are using [TD-Survey](https://github.com/hjmsano/td-survey), the survey result will be recorded with these action/category pair.|


## 拡張によって計測されたデータに対するクエリー

### 日別ページビュー数とユニークブラウザ数

```sql
SELECT
  TD_TIME_FORMAT(time,
    'yyyy-MM-dd',
    'JST') AS date_time,
  COUNT(*) AS pageviews,
  COUNT(DISTINCT td_client_id) AS unique_browsers
FROM
  your_database.weblog  -- 変更してください
WHERE
  TD_TIME_RANGE(time,
    DATE_FORMAT(DATE_ADD('hour',
      9 - (24 * 30),  -- 日本時間で過去30日
      NOW()),
      '%Y-%m-%d %H:%i:%s'),
    NULL,
    'JST')
  AND action = 'view'
  AND category = 'page'
GROUP BY
  1
;
```

### トップページのスクロール深度

```sql
SELECT
  SUM(CASE
      WHEN (scroll_depth >= 20) THEN 1 ELSE 0 END) AS "20p",
  SUM(CASE
      WHEN (scroll_depth >= 40) THEN 1 ELSE 0 END) AS "40p",
  SUM(CASE
      WHEN (scroll_depth >= 60) THEN 1 ELSE 0 END) AS "60p",
  SUM(CASE
      WHEN (scroll_depth >= 80) THEN 1 ELSE 0 END) AS "80p",
  SUM(CASE
      WHEN (scroll_depth >= 100) THEN 1 ELSE 0 END) AS "100p"
FROM (
    SELECT
      root_id,
      MAX(scroll_depth) AS scroll_depth
    FROM
      your_database.weblog  -- 変更してください
    WHERE
      TD_TIME_RANGE(time,
        DATE_FORMAT(DATE_ADD('hour',
          9-24,  -- 日本時間で過去24時間
          NOW()),
          '%Y-%m-%d %H:%i:%s'),
        NULL,
        'JST')
      AND action = 'scroll'
      AND category = 'page'
      AND td_path = '/'
    GROUP BY
      root_id
  )
;
```

### 記事別読了率 （読了は 10秒以上かつ80%以上）

```sql
SELECT
  td_title,
  SUM(CASE WHEN action = 'view' THEN 1 ELSE 0 END) AS pageviews,
  SUM(CASE WHEN action = 'read' THEN 1 ELSE 0 END) AS read_complete
FROM (
    SELECT
      td_title,
      root_id,
      action,
      MAX(read_rate) AS read_depth
    FROM
      your_database.weblog -- 変更してください
    WHERE
      TD_TIME_RANGE(time,
        DATE_FORMAT(DATE_ADD('hour',
          9-24, -- 日本時間で過去24時間
          NOW()),
          '%Y-%m-%d %H:%i:%s'),
        NULL,
        'JST')
      AND(
        (
          action = 'read'
          AND category = 'content'
          AND read_elapsed_ms >= 10000
          AND read_rate >= 80
        )
        OR (
          action = 'view'
          AND category = 'page'
        )
      )
    GROUP BY
      td_title,
      root_id,
      action
  )
GROUP BY
  td_title
;
```

### メディアファイル別メディア (ビデオ & オーディオ) 再生分析

```sql
SELECT
  media_src AS media,
  CASE
    WHEN played_percent >= 100 THEN '100p'
    WHEN played_percent >= 80 THEN '80p'
    WHEN played_percent >= 60 THEN '60p'
    WHEN played_percent >= 40 THEN '40p'
    WHEN played_percent >= 20 THEN '20p'
    WHEN played_percent < 20 THEN 'less_than_20'
    ELSE 'unknown'
  END AS played,
  COUNT(*) AS views
FROM (
    SELECT
      media_src,
      root_id,
      MAX(media_played_percent) AS played_percent
    FROM
      your_database.weblog -- 変更してください
    WHERE
      TD_TIME_RANGE(time,
        DATE_FORMAT(DATE_ADD('hour',
            9-24, -- 日本時間で過去24時間
            NOW()),
          '%Y-%m-%d %H:%i:%s'),
        NULL,
        'JST')
      AND action IN(
        'timeupdate',
        'ended'
      )
      AND category = 'video'
      AND media_src != ''
    GROUP BY
      media_src,
      root_id
  )
GROUP BY
  1,
  2
;
```

### ページごとの滞在時間の中央値

```sql
SELECT
  td_path,
  APPROX_PERCENTILE(
    elapsed_ms,
    0.5
  ) / 1000 AS median_time_spent_sec
FROM (
    SELECT
      root_id,
      td_path,
      MAX(since_init_ms) AS elapsed_ms
    FROM
      your_database.weblog -- 変更してください
    WHERE
      TD_TIME_RANGE(time,
        DATE_FORMAT(DATE_ADD('hour',
            9-24, -- 日本時間で過去24時間
            NOW()),
          '%Y-%m-%d %H:%i:%s'),
        NULL,
        'JST')
      AND action = 'scroll'
      AND category = 'page'
    GROUP BY
      root_id,
      td_path
  )
GROUP BY
  td_path
;
```

### トップページにおける時間別RUM

```sql
SELECT
  TD_TIME_FORMAT(time,
    'yyyy-MM-dd HH:00:00',
    'JST') AS date_time,
  CASE
  WHEN performance_dcl < 1000 THEN 'less_than_1sec'
  WHEN (performance_dcl >= 1000 AND performance_dcl < 2000) THEN '1-2sec'
  WHEN (performance_dcl >= 2000 AND performance_dcl < 4000) THEN '2-4sec'
  WHEN (performance_dcl >= 4000 AND performance_dcl < 7000) THEN '4-7sec'
  WHEN (performance_dcl >= 7000 AND performance_dcl < 10000) THEN '7-10sec'
  WHEN performance_dcl > 10000 THEN 'more_than_10sec'
  ELSE 'unknown' END as dom_content_loaded,
  COUNT(*) AS pageviews
FROM
  your_database.weblog  -- 変更してください
WHERE
  TD_TIME_RANGE(time,
    DATE_FORMAT(DATE_ADD('hour',
      9 - (24 * 7), -- 日本時間で過去7日
      NOW()),
      '%Y-%m-%d %H:%i:%s'),
    NULL,
    'JST')
  AND action = 'rum'
  AND category = 'page'
  AND td_path = '/'
GROUP BY
  1,2
;
```

## ライセンスと著作権
この拡張は [Ingestly Tracking JavaScript](https://github.com/ingestly/ingestly-client-javascript) からフォークしました。
