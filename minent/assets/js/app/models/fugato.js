/**
 *  app/models/fugato.js
 *  Models for Fugato (Questions and Answers)
 *
 *  Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
 *  Created:  Thu Oct 30 13:43:41 2014 -0400
 *
 *  Copyright (C) 2014 University of Maryland
 *  For license information, see LICENSE.txt
 *
 *  ID: fugato.js [] bengfort@cs.umd.edu $
 */

// JS Hint directives and strict mode
/* globals exports,__filename */
'use strict';

define([
  "backbone",
  "underscore"
], function(Backbone, _) {

  // Question Model
  var QuestionModel = Backbone.Model.extend({
    defaults: {
      text: null,
      author: null,
      created: null,
      modified: null
    }
  });

  var QuestionCollectionMeta = Backbone.Collection.extend({
    defaults: {
      count: 0,
      next: null,
      previous: null
    }
  });

  var QuestionCollection = Backbone.Collection.extend({
    url: "/api/questions/",
    model: QuestionModel,
    comparator: function(m) {
      return -Date.parse(m.get('created'));
    },

    initialize: function() {
      this.meta = new QuestionCollectionMeta();
    },

    parse: function(data) {
      var results = data.results;
      delete data.results;
      this.meta.set(data);
      return results;
    },

    sync: function() {
      return Backbone.sync.apply(Backbone, arguments);
    }

  });

  QuestionCollection.QuestionModel = QuestionModel;
  QuestionCollection.QuestionCollectionMeta = QuestionCollectionMeta;
  return QuestionCollection;

});
