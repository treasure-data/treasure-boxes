# Extension for Treasure Data's TD-JS-SDK

[Japanese document available here / 日本語のドキュメントはこちら](README-JP.md)

**Notice: Please note that this library is NOT a product of Treasure Data. At Your Own Risks please.**

## Installation

First of all, see `/example/index.html`. It helps you to understand the installation.

1. Embed TD-JS-SDK loader in your html file. This is the same process as [official TD-JS-SDK implementation](https://github.com/treasure-data/td-js-sdk#installing).
**DO NOT follow other than this first step. YOU DO NOT need `new Treasure()` and other codes because everything is in `config.js`.**

```html
<!-- Treasure Data -->
<script type="text/javascript">
!function(t,e){if(void 0===e[t]){e[t]=function(){e[t].clients.push(this),this._init=[Array.prototype.slice.call(arguments)]},e[t].clients=[];for(var r=function(t){return function(){return this["_"+t]=this["_"+t]||[],this["_"+t].push(Array.prototype.slice.call(arguments)),this}},s=["blockEvents","setSignedMode","fetchServerCookie","unblockEvents","setSignedMode","setAnonymousMode","resetUUID","addRecord","fetchGlobalID","set","trackEvent","trackPageview","trackClicks","ready"],n=0;n<s.length;n++){var o=s[n];e[t].prototype[o]=r(o)}var c=document.createElement("script");c.type="text/javascript",c.async=!0,c.src=("https:"===document.location.protocol?"https:":"http:")+"//cdn.treasuredata.com/sdk/2.2/td.min.js";var i=document.getElementsByTagName("script")[0];i.parentNode.insertBefore(c,i)}}("Treasure",this);
</script>
```

2. Embed two files in `/dist` directory. One is a core file of this extension, another one is configuration and initialization file.
  - `td-js-sdk-ext.js` is a core library of the extension
  - `config.js` contains everything you need for measurement

```html
<script src="td-js-sdk-ext.js"></script>
<script src="config.js"></script>
```

3. Modify `config.js` by following the below Configuration section.


## Configuration

### TreasureData Standard Configuration Variables

In the top of `config.js`, you can see lines for TD-JS-SDK initialization like `var td = new Treasure({...});`.
This is a standard configuration process for TD-JS-SDK so set each variables by referring the [official reference in TD-JS-SDK Readme](https://github.com/treasure-data/td-js-sdk#treasureconfig).

### Extension Specific Configuration Variables

A few lines after `new Treasure({...})`, there is another initialization method call like `tdext.init({...})`.
You can control what to be measured and granularity of events.

|variable|example|description|
|:---|:---|:---|
|`table`|`weblog`|A table name for storing all data measured by the extension|
|`eventName`|`TDExtRecurringEvent`|The extension dispatches a recurring event to observe element visibility. Change an event name if needed.|
|`eventFrequency`|`250`|A throttling interval for the recurring event. This is linked to the data accuracy and the user experience.|
|`targetWindow`|`self`|A frame to be observed but basically this should be `self` because TD-JS-SDK does not work in iframe properly.|
|`tdNs`|`td`|A namespace of TD-JS-SDK object.|

### Session ID support

- Not a few web analyst still uses "Session" based behavior aggregation, and it requires an SQL skills if records don't have a session ID.
- This SDK can set a session ID and collect it by setting `true` to `options.session.enable`, and you can use additional options below:

|variable|example|description|
|:---|:---|:---|
|domain|`example.com`|A domain name to be set as an issuer of the cookie. If you want to share the cookie across multiple sub-domains, set a parent domain.|
|lifetime|`1800`|A cookie lifetime in seconds. If the visitor does not send beacons over this value, session will be renewd on the next page.|

- Note that this feature uses a cookie named `tdextSesId`.

#### Time-spent on a page (unload)

- Unload tracking set an eventListener to one of available events when the page is being unloaded.
- You can get an exact time that user spent during the specific pageview.
- In `tdext.init()`, set `true` for `options.unload.enable`.

#### Clicks Tracking

- Click tracking is triggered if the clicked element (or its parent) has the specified `data-*` attribution.
- If you omit `options.clicks.targetAttr` but `options.clicks.enable` is `true`, Click tracking will measure clicks on elements without `data-*` attribution. 
- In `tdext.init()`, set `true` for `options.clicks.enable` and adjust values:

|variable|example|description|
|:---|:---|:---|
|`targetAttr`|`data-trackable`|attribution name for identifying the target element|

- If you set `data-trackable` for `targetAttr`, you need to add `data-trackable` attribution to every element you want to track clicks.
- Ideally, every block elements should be structured like hierarchy. and each block element should have `data-trackable` with meaningful value.

#### Scroll Depth

- Scroll depth tracking for both fixed page and infinity scroll (lazy-load) page.
- In `tdext.init()`, set `true` for `options.scroll.enable` and adjust values:

|variable|example|description|
|:---|:---|:---|
|`threshold`|`2`|track the depth when the user stay at/over N percent/pixels for more than X seconds specified here|
|`granularity`|`20`|track the depth every X percent/pixels increased|
|`unit`|`percent`|for the fixed height page, you can use `percent`. If the page is infinity scroll, use `pixels` instead|

#### Read-Through Rate

- Read-Through Rate means is a metrics that describes how much range of content is consumed by an user.
- In `tdext.init()`, set `true` for `options.read.enable` and adjust values:

|variable|example|description|
|:---|:---|:---|
|`threshold`|`4`|track the depth of content when the user keep staying at/over N percent for more than X seconds|
|`granularity`|`10`|track the rate every X percent increased|
|`target`|`document.getElementById('article')`|An element which contains article body (content). Specify a block elements to be observed as a target of read-through.|

#### Media Tracking

- Once you enabled this option, all media which is VIDEO or AUDIO will be tracked automatically.
- This option supports `play`, `pause` and `eneded` events plus the heart-beat.
- In `tdext.init()`, set `true` for `options.media.enable` and adjust values:

|variable|example|description|
|:---|:---|:---|
|`heartbeat`|`5`|the heart-beat tracker will be dispatched every X sec defined here|

#### Form Analysis

- Form Analysis provides a statistics info regarding the form completion but not values of form fields.
- This feature accepts multiple forms by passing a list of target element of forms.
- In `tdext.init()`, set `true` for `options.form.enable` and adjust values:

|variable|example|description|
|:---|:---|:---|
|`targets`|`document.getElementsByTagName('form')`|A list of form elements.|


## Methods

### tdext.trackPageview(context, successCallback, failureCallback)

- Track a pageview event
- Any parameters are optional.

|parameter|example|description|
|:---|:---|:---|
|`context`|`{name: "hoge"}`|An object of custom context for the event.|
|`successCallback`|`function(){}`|A method name or a method to be triggered just after sending data is succeeded|
|`failureCallback`|`function(){}`|A method name or a method to be triggered just after sending data is failed|

### tdext.trackAction(action, category, context, successCallback, failureCallback)

- Track a custom event
- Any parameters are optional but `action` and `category` are strongly recommended to be defined.

|parameter|example|description|
|:---|:---|:---|
|`action`|`toggle`|An action name.|
|`category`|`switch`|A target being applied the action.|
|`context`|`{name: "hoge"}`|An object of custom context for the event.|
|`successCallback`|`function(){}`|A method name or a method to be triggered just after sending data is succeeded|
|`failureCallback`|`function(){}`|A method name or a method to be triggered just after sending data is failed|

### tdext.trackRead(target)

- Initialize the Read-Through tracking
- If your page uses the lazy-load (infinity scroll and append another content ondemandly), you should re-initialize by `trackRead()` to measure the newly added article.

|parameter|example|description|
|:---|:---|:---|
|`target`|`document.getElementById('article')`|A block element which contains an article body (content).|


## Action and Category combination

|Action|Category|Description|
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


## Querying data measured by the Extension

### Daily Pageviews & Unique Browsers

```sql
SELECT
  TD_TIME_FORMAT(time,
    'yyyy-MM-dd',
    'JST') AS date_time,
  COUNT(*) AS pageviews,
  COUNT(DISTINCT td_client_id) AS unique_browsers
FROM
  your_database.weblog  -- CHANGE HERE
WHERE
  TD_TIME_RANGE(time,
    DATE_FORMAT(DATE_ADD('hour',
      9 - (24 * 30),  -- Last 30 days in JST
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

### Scroll Depth on front page

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
      your_database.weblog  -- CHANGE HERE
    WHERE
      TD_TIME_RANGE(time,
        DATE_FORMAT(DATE_ADD('hour',
          9-24,  -- Last 24 hours in JST
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

### Read-Through Rate per an article (Read Complete is > 10sec && 80%)

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
      your_database.weblog -- CHANGE HERE
    WHERE
      TD_TIME_RANGE(time,
        DATE_FORMAT(DATE_ADD('hour',
          9-24, -- Last 24 hours in JST
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

### Media (Video & Audio) playback analysis per a media file

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
      your_database.weblog -- CHANGE HERE
    WHERE
      TD_TIME_RANGE(time,
        DATE_FORMAT(DATE_ADD('hour',
            9-24, -- Last 24 hours in JST
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

### Median time-spent per a page

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
      your_database.weblog -- CHANGE HERE
    WHERE
      TD_TIME_RANGE(time,
        DATE_FORMAT(DATE_ADD('hour',
            9-24, -- Last 24 hours in JST
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

### Hourly RUM for front page

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
  your_database.weblog  -- CHANGE HERE
WHERE
  TD_TIME_RANGE(time,
    DATE_FORMAT(DATE_ADD('hour',
      9 - (24 * 7), -- Last 7 days in JST
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

## License and Copyright
This extension is forked from [Ingestly Tracking JavaScript](https://github.com/ingestly/ingestly-client-javascript).
