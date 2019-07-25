(function () {
  // version 0.2.0 for Brightcove player vesion6
  'use strict';
  var _indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  videojs.registerPlugin('td', function(options) {
    if (!options.writeKey || !options.database || !options.table ) {
      videojs.log("require writeKey, database, table");
      return;
    }
    var referrer, TdLogger, player, tdLogger,trackEventList,defaultTrackEventList, percentsAlreadyTracked, getInterval, interval, seekStart, seekEnd, eventNameLabels, getVideo, seeking, loaded,
    ended, play, pause, error, fullScreenChange, volumeChange, percentOfView, seek;
    referrer = document.createElement('a');
    referrer.href = document.referrer;
    if (self !== top && ((window.location.host === 'players.brightcove.net' || window.location.host === 'preview-players.brightcove.net') && referrer.hostname === 'studio.brightcove.com')) {
      videojs.log('TreasureData plugin will not track events in Video Cloud Studio');
      return;
    }
    player = this,
    TdLogger = function(options) {
      this.td = new TreasureVideojs({
        host: options.host || 'in.treasuredata.com',
        writeKey : options.writeKey,
        database : options.database,
        startInSignedMode: options.startInSignedMode || false
      });
      this.table = options.table;
      this.debug = options.debug || false;
      this.td.set(this.table, {'bc_video_id':player.tagAttributes['data-video-id']});
      if (options.trackCrossDomain) {
        this.td.set('$global', 'td_global_id', 'td_global_id');
      }
      this.log = function(type, params) {
        if(typeof params === 'undefined') {
          params = {};
        }
        params.bc_event = type;
        if (!this.debug) {
          this.td.trackEvent(this.table, params);
        } else {
          videojs.log("Table name is " + this.table +", params are as follows.");
          videojs.log(params);
        }
      };
    },
    tdLogger = new TdLogger(options),
    getInterval = function(options) {
      var intervalList = [5, 10, 25], i = 10;
      if(typeof options.interval !== 'undefined' && _indexOf.call(intervalList, options.interval) >= 0) {
        i = options.interval;
      }
      return i;
    },
    interval = getInterval(options),
    defaultTrackEventList = ['play', 'pause','error','fullscreen_change','volume_change','ended','percent_of_view','seek','player_load', 'video_loaded'],
    trackEventList = options.trackEventList || defaultTrackEventList;
    if (trackEventList.length === 0) {
      trackEventList = defaultTrackEventList;
    }
    percentsAlreadyTracked = [], seekStart = 0, seekEnd = 0, seeking = false,
    eventNameLabels = {
      'player_load' : 'Player Loaded',
      'video_loaded' : 'Contents Loaded',
      'play' : 'Play',
      'pause' : 'Pause',
      'error' : 'Error',
      'fullscreenchange' : 'FullScreen Start',
      'fullscreenchangeexit' : 'FullScreen Exit',
      'volumechange' : 'Volume Change',
      'ended':'Complete',
      'percent_of_view' : 'Percent of View',
      'seek' : 'Seek'
    };
    if (options.eventNameLabels && Object.keys(options.eventNameLabels).length > 0) {
      var labelKeys = Object.keys(options.eventNameLabels), len = labelKeys.length;
      for (var i = 0; i < len; i++) {
        eventNameLabels[labelKeys[i]] = options.eventNameLabels[labelKeys[i]];
      }
    }
    loaded = function() {
      tdLogger.log(eventNameLabels.video_loaded);
    },
    ended = function() {
      tdLogger.log(eventNameLabels.ended);
    },
    play = function() {
      tdLogger.log(eventNameLabels.play);
      seeking = false;
    },
    pause = function() {
      tdLogger.log(eventNameLabels.pause);
      seeking = false;
    },
    error = function() {
      tdLogger.log(eventNameLabels.error);
    },
    fullScreenChange = function() {
      if(this.isFullscreen()) {
        tdLogger.log(eventNameLabels.fullscreenchange);
      } else {
        tdLogger.log(eventNameLabels.fullscreenchangeexit);
      }
    },
    volumeChange = function() {
      var volume;
      volume = this.muted() === true ? 0 : this.volume();
      tdLogger.log(eventNameLabels.volumechange, {'bc_volume':volume});
    },
    percentOfView =function() {
      var currentTime, duration, percent, percentOfViewed, _i;
        currentTime = Math.round(this.currentTime());
        duration = Math.round(this.duration());
        percentOfViewed = Math.round(currentTime / duration * 100);
        for (percent = _i = 0; _i <= 100; percent = _i += interval) {
          if (percentOfViewed >= percent && _indexOf.call(percentsAlreadyTracked, percent) < 0) {
            tdLogger.log(eventNameLabels.percent_of_view, {'bc_percent':percent});
            percentsAlreadyTracked.push(percent);
          }
      }
    },
    seek = function() {
      var currentTime = Math.round(this.currentTime());
      seekStart = seekEnd;
      seekEnd = currentTime;
      if (Math.abs(seekStart - seekEnd) > 1) {
        seeking = true;
        tdLogger.log(eventNameLabels.seek, {'bc_seek_start':seekStart, 'bc_seek_end': seekEnd});
      }
    },
    this.ready(function() {
      if (_indexOf.call(trackEventList, 'player_load') >= 0) {
        tdLogger.log(eventNameLabels.player_load);
      }
      if (_indexOf.call(trackEventList,'video_loaded') >= 0) {
        player.on('loadedmetadata', loaded);
      }
      if (_indexOf.call(trackEventList,'play') >= 0) {
        player.on('play', play);
      }
      if (_indexOf.call(trackEventList,'pause') >= 0) {
        player.on('pause', pause);
      }
      if (_indexOf.call(trackEventList, 'error') >= 0) {
        player.on('error', error);
      }
      if (_indexOf.call(trackEventList, 'fullscreen_change') >= 0) {
        player.on('fullscreenchange', fullScreenChange);
      }
      if (_indexOf.call(trackEventList, 'volume_change') >= 0) {
        player.on('volumechange', volumeChange);
      }
      if (_indexOf.call(trackEventList, 'percent_of_view') >= 0) {
        player.on('timeupdate', percentOfView);
      }
      if (_indexOf.call(trackEventList, 'seek') >= 0) {
        player.on('timeupdate', seek);
      }
      if (_indexOf.call(trackEventList, 'ended') >= 0) {
        player.on('ended', ended);
      }
    });
  });
}).call(this);
