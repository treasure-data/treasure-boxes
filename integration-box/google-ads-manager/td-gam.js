<!-- SAMPLE -->
<script async src="//www.googletagservices.com/tag/js/gpt.js"></script>

<script>
  !function(t,e){if(void 0===e[t]){e[t]=function(){e[t].clients.push(this),this._init=[Array.prototype.slice.call(arguments)]},e[t].clients=[];for(var r=function(t){return function(){return this["_"+t]=this["_"+t]||[],this["_"+t].push(Array.prototype.slice.call(arguments)),this}},s=["addRecord","set","trackEvent","trackPageview","trackClicks","ready","fetchUserSegments"],a=0;a<s.length;a++){var c=s[a];e[t].prototype[c]=r(c)}var n=document.createElement("script");n.type="text/javascript",n.async=!0,n.src=("https:"===document.location.protocol?"https:":"http:")+"//cdn.treasuredata.com/sdk/2.1.0/td.min.js";var i=document.getElementsByTagName("script")[0];i.parentNode.insertBefore(n,i)}}("Treasure",this);

  var td = new Treasure({
    host: 'in.treasuredata.com',
    writeKey: 'WRITEAPIKEY',
    database: 'DBNAME',
    startInSignedMode: true
  });

  var cdp_token = 'PROFILE_TOKEN';

  var googletag = window.googletag || {cmd: []};

  googletag.cmd.push(function() {
    googletag.defineSlot('XXXXXX', ['XXXXXX', [320, 50], [320, 100], [320, 180]], 'XXXXXX').addService(googletag.pubads());
    //googletag.defineSlot('YYYYYY', ['YYYYYY', [320, 50], [320, 100], [320, 180]], 'YYYYYY').addService(googletag.pubads());
    googletag.pubads().enableSingleRequest();
  });

  var successCallback = function(audiences) {
    var segments = [];
    var attributes = [];
    for (var i = 0; i < audiences.length; i++) {
      var seg = audiences[i].values || [];
      segments = segments.concat(seg);

      var attrs = audiences[i].attributes || [];
      for (let key in attrs) {
        let val = attrs[key];
        if (Array.isArray(val)) {
          for (let i = 0; i < val.length; i++) {
            if (val[i]) {
              attributes = attributes.concat(val[i]);
            }
          }
        } else if (val) {
         attributes = attributes.concat(val);
        }
      }
    }

    var area = (/ar[0-9]{4}/g.exec(location.pathname));
    area = (area == null)? '' : area[0];

    googletag.cmd.push(function() {
      googletag.pubads().setTargeting('XXXXXX', segments);
      //googletag.pubads().setTargeting('YYYYYY', attributes);
      googletag.pubads().enableLazyLoad({
        fetchMarginPercent: 200,
        renderMarginPercent: 100,
        mobileScaling: 2.0
      });
      googletag.enableServices();
      googletag.display('AAAAAA');
      //googletag.display('BBBBBB');
    });
  };

  var errorCallback = function(err) {
    console.error(err);
  };

  var getcookie=function(a){var b=document.cookie;if(b)for(var c=b.split("; "),d=0;d<c.length;d++){var b=c[d].split("=");if(b[0]===a)return b[1]}return"null"};

  td.fetchUserSegments({
    audienceToken: [cdp_token],
    keys: {
      td_client_id: getcookie('_td')
    }
  }, successCallback, errorCallback);
</script>
