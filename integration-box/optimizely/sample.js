<html>
<head>
  <meta charset="utf-8">
  <title>optimizely test</title>
  <script type="text/javascript">
// loading TreasureData SDK
!function(t,e){if(void 0===e[t]){e[t]=function(){e[t].clients.push(this),this._init=[Array.prototype.slice.call(arguments)]},e[t].clients=[];for(var r=function(t){return function(){return this["_"+t]=this["_"+t]||[],this["_"+t].push(Array.prototype.slice.call(arguments)),this}},s=["blockEvents","unblockEvents","setSignedMode","setAnonymousMode","resetUUID","addRecord","fetchGlobalID","fetchUserSegments","set","trackEvent","trackPageview","trackClicks","ready"],n=0;n<s.length;n++){var c=s[n];e[t].prototype[c]=r(c)}var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=("https:"===document.location.protocol?"https:":"http:")+"//cdn.treasuredata.com/sdk/2.1/td.min.js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)}}("Treasure",this);
  </script>
<script type="text/javascript">
  var self = this;
  var createScript = function(a) {
    var b = document.createElement("script");
    b.type = "text/javascript", b.async = !0, b.src = a;
    var d = document.getElementsByTagName("script")[0];
    d.parentNode.insertBefore(b, d.nextSibling)
  };
  var fetchCallback = function(res) {
    // load your Optimizely snippet
    var value = res[0].values;
    self.Window.td_seg_ids=value;
    createScript("YOUR SNIPPET CODE URL");
  };
  var td = new Treasure({
    host: 'YOUR_JSSDK_ENDPOINT',
    writeKey: 'YOUR_API_KEY',
    database: 'DATABASE',
    startInSignedMode: true
  });
  var token = 'YOUR_PERSONALIZATION_TOKEN';
  // fetching user segment from Profile API
  td.fetchUserSegments(token, fetchCallback, err);
  var err = function(error) {
    console.log("error callback");
  }
  </script>
</head>
<body>
 
<div id='container'>
<h1 style="color:black">Optimizely Integration Test</h1>
<div><a href="https://www.treasuredata.co.jp/customers/" target="_blank">Customers page</a></div>
</div>
<script type="text/javascript">
  td.trackPageview('TABLE');
</script>
</body>
</html>