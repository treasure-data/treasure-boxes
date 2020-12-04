function trackerAcceptanceProcess() {
 // put your TD tag here.



}

(function() {
  function readCookie(key) {
    return ((';' + document.cookie + ';').match(';' + key + '=([^\S;]*)') || [])[1];
  };

  if (readCookie('_td_accept') === '1') {
    trackerAcceptanceProcess();
  } else {
    var dialogDiv = document.createElement('div');
    dialogDiv.style = 'position: fixed; bottom: 0; right: 0; width: 260px; margin: 0px; padding: 20px; border: 1px solid #ccc; background: #555; color: #ccc; font-size: 10pt';
    dialogDiv.innerHTML = '<p>Please support us to measure our service quality. To make our service better, we would like to use TreasureData and its Cookies.</p>';
    dialogDiv.innerHTML += '<button onClick="document.cookie=\'_td_accept=1\';trackerAcceptanceProcess();this.parentElement.remove();">Accept</button>';
    var scriptTag = document.currentScript || (function() {
      var tags = document.getElementsByTagName('script')
      return tags.item(tags.length - 1)
    }());
    document.getElementsByTagName('body')[0].insertBefore(dialogDiv, scriptTag);
  }
}());
