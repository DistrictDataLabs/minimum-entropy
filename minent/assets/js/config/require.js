/**
 * config/require.js
 * Configuration for Require.js
 *
 * Copyright (C) 2016 District Data Labs
 * For license information, see LICENSE.txt
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Wed Jan 22 23:52:24 2014 -0500
 *
 * ID: require.js [] benjamin@bengfort.com $
 */

requirejs.config({
  baseUrl: '/assets/js',
  paths: {
    'underscore': '//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min',
    'jquery': '//code.jquery.com/jquery-1.11.3.min',
    'bootstrap': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min',
    'backbone': '//cdnjs.cloudflare.com/ajax/libs/backbone.js/1.2.1/backbone-min',
    'text': '//cdnjs.cloudflare.com/ajax/libs/require-text/2.0.12/text.min',
    'mustache': '//cdnjs.cloudflare.com/ajax/libs/mustache.js/2.1.2/mustache.min',
    'moment': '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.3/moment.min',
    'typeahead': '//cdnjs.cloudflare.com/ajax/libs/typeahead.js/0.11.1/typeahead.bundle.min',
  },
  shim: {
    'underscore': {
      exports: '_'
    },
    'jquery': {
      exports: '$'
    },
    'backbone': {
      deps: ['jquery', 'underscore'],
      exports: 'Backbone'
    },
    'bootstrap': {
      deps: ['jquery']
    },
    'typeahead': {
      deps: ['jquery'],
      exports: 'Bloodhound'
    }
  }
});
