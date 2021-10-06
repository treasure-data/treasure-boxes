<html>
<head>
  <meta charset="utf-8">
  <title>optimizely test</title>
  <script type="text/javascript">
  var self = this;
  var createScript = function(a) {
    var b = document.createElement("script");
    b.type = "text/javascript", b.async = !0, b.src = a;
    var d = document.getElementsByTagName("script")[0];
    d.parentNode.insertBefore(b, d)
  };
  var fetchCallback = function(res) {
    var value = res[0].values;
    self.Window.td_seg_ids=value;
    // load your Optimizely snippet
    createScript("YOUR SNIPPET CODE URL");
  };
  // calling profile API directly
  var url = 'https://cdp.in.treasuredata.com/cdp/lookup/collect/segments?version=2&amp;token=<YOUR TOKEN>&callback=fetchCallback';
  createScript(url);
  </script>
</head>
<body>
 
<div id='container'>
<h1 style="color:black">Optimizely Integration Test</h1>
<div><a href="https://www.treasuredata.co.jp/customers/" target="_blank">Customers page</a></div>
</div>
</body>
</html>