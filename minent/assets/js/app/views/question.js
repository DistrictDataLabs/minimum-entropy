define([
    'backbone',
    'underscore',
    'text!../templates/question.html'
],
function(Backbone, _, questionHtml) {

    var QuestionView = Backbone.View.extend({
      tagName: "li",
      template: _.template(questionHtml),

      render: function() {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
      }

    });

    return QuestionView;

});
