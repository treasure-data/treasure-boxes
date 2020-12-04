// Put your TD tag here



 // Wrapper for TD's optoup method
function optoutTd(){
  td.blockEvents();
}

(function() {
  function readCookie(key) {
    return ((';' + document.cookie + ';').match(';' + key + '=([^\S;]*)') || [])[1];
  };

  var optoutFlag = readCookie('_td_optout');
  if (optoutFlag !== '0' && optoutFlag !== '1' ) {
    var dialogDiv = document.createElement('div');
    dialogDiv.style = 'position: fixed; bottom: 0; right: 0; width: 260px; margin: 0px; padding: 20px; border: 1px solid #ccc; background: #555; color: #ccc; font-size: 10pt';
    dialogDiv.innerHTML = '<p>Please support us to measure our service quality. Your usage is measured but you can opt-out by clicking the below button. </p>';
    dialogDiv.innerHTML += '<button onClick="document.cookie=\'_td_optout=1\';optoutTd();this.parentElement.remove();">Optout</button> <button onClick="document.cookie=\'_td_optout=0\';this.parentElement.remove();">Continue</button>';
    var scriptTag = document.currentScript || (function() {
      var tags = document.getElementsByTagName('script')
      return tags.item(tags.length - 1)
    }());
    document.getElementsByTagName('body')[0].insertBefore(dialogDiv, scriptTag);
  }
}());
