define(
function(require, exports, module) {

  var Backbone = require('backbone');
  var _ = require('underscore');
  var QuestionCollection = require('../models/fugato')
  var QuestionView = require('./question');

  var QuestionListView = Backbone.View.extend({

    el: "#questionApp",

    initialize: function() {
      this.input = this.$('input#query');
      this.questions = new QuestionCollection;
      this.views = [];

      this.listenTo(this.questions, "sync", this.render);
      this.listenTo(this.questions, "remove", function() { this.questions.fetch(); });
      this.questions.fetch();
    },

    submitQuestion: function(event) {
      event.preventDefault();
      var query = this.input.val();

      if (!query) { return; }

      this.questions.create({text:query}, {wait:true});
      this.input.val('');

      return false;
    },

    render: function() {
      var ul = this.$("#question-list");
      _.invoke(this.views, "remove");
      this.views.length = 0;

      this.questions.each(function(model, idx) {
        var item = new QuestionView({model:model});
        item.render();
        ul.append(item.$el);
        this.views.push(item);
      }, this);
    },

    events: {
      "submit form": "submitQuestion"
    }

  });

  return QuestionListView;

});
