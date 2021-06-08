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
  init(options) {
    console.log("init:", options);
    td = new Treasure(options);
    console.log("instance:", td);
  },
};
