/*
 * Main entry point to the Minimum Entropy application
 */

define([
  './models/fugato',
  './views/list'
],
function(QuestionCollection, QuestionListView) {

  var view = new QuestionListView();

  return {
    view: view,

    start: function() {
      // Do the CSRf AJAX Modification
      var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
      $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});

      console.log("Minimum Entropy is started and ready");
    },

    stop: function() {
      console.log("Minimum Entropy has stopped")
    }
  }

});
