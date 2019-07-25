# Videojs-plugin-td

This is a plugin for Brightcove player(videojs).
User can import the event log on the Brightcove player to TreasureData by using this.
This plugin support single movie creative and some Gallary-In-Page creatives.
As of 2019-7-2, we supported for Grid and Carousel type of creative.

## Which event can this plugin import?

* Player Loaded
* Content Loaded
* Play
* Pause
* Error
* Start FullScreen
* End FullScreen
* Volume Change
* End the content
* Percent of View
* Seek

## Log detail

In Addition to [default params of TreasureData Javascript SDK](https://docs.treasuredata.com/articles/javascript-sdk#step-2-initialize-amp-send-events-to-the-cloud), Each event logs as follows parameters.

|`bc_event` column|additional column|example|
|:---:|:---:|:---:|
|Player Loaded|||
|Contents Loaded|||
|Play|bc_duration|`39.11`|
|Pause|||
|Error|||
|FullScreen Start|||
|FullScreen Exit|||
|Volume Change|bc_volume|`0`, `1`, `0.91111`|
|Complete|||
|Percent of View|bc_percent|`5`,`25`|
|Seek|bc_seek_start,bc_seek_end|`1`,`3`, `10`|

Addition to the above items, the plugin put some items into the log.

* bc_video_id : video id
* bc_session_id : session id
* bc_video_name : video name
* bc_duration : video length

## Options

This plugin can use some options.

|Name|Required?|Description|Default|
|:---:|:---:|:---|:---|
|writeKey|Required|TreasureData API writeKey||
|database|Required|TreasureData Database Name||
|table|Required|TreasureData Table Name||
|host||TreasureData Import API Hostname|`in.treasuredata.com`|
|trackCrossDomain||Enable cross-domain tracking|`false`|
|startInSignedMode||set sighedmode true|`false`|
|interval||Interval percent number of view. can select from [5 or 10 or 25]|`10`|
|trackEventList||can select track event|`'play','pause','error','fullscreen_change','volume_change','ended', 'percent_of_view','seek','player_load', 'video_loaded'`|
|eventNameLabels||can set event name to each event|`'player_load' : 'Player Loaded','video_loaded' : 'Contents Loaded', 'play' : 'Play', 'pause' : 'Pause', 'error' : 'Error', 'fullscreenchange' : 'FullScreen Start','fullscreenchangeexit' : 'FullScreen Exit', 'volumechange' : 'Volume Change', 'ended':'Complete','percent_of_view' : 'Percent of View', 'seek' : 'Seek'`|


