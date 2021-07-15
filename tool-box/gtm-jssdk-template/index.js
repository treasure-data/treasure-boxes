var Treasure = require("td-js-sdk");

var td = null;

module.exports = {
  trackPageview: function (table) {
    td.trackPageview(table);
  },
  setSignedMode: function () {
    td.setSignedMode();
  },
  setAnonymousMode: function () {
    td.setAnonymousMode();
  },
  setGlobalId: function () {
    td.set("$global", "td_global_id", "td_global_id");
  },
  fetchGlobalID: function () {
    td.fetchGlobalID();
  },
  fetchServerCookie(force) {
    return new Promise(function(resolve, reject) {
      td.fetchServerCookie(resolve, reject, force)
    });
  },
  setServerCookie: function(sscId){
    td.set('$global', { td_ssc_id: sscId });
  },
  init(options) {
    td = new Treasure(options);
  },
};
