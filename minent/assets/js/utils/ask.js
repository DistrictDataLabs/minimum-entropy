/**
 * utils/ask.js
 * Javascript that runs the ask question dialogs
 *
 * Copyright (C) 2016 District Data Labs
 * For license information, see LICENSE.txt
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Fri Jan 16 11:48:50 2015 -0500
 *
 * ID: hotkeys.js [] benjamin@bengfort.com $
 */


(function($) {
    $(document).ready(function() {

        var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});
        console.log("ask application ready");

        // Form elements for ease of handling
        var askQuestionModal   = $("#askQuestionModal");
        var askQuestionForm    = $("#askQuestionForm");
        var txtQuestion        = $("#txtQuestion");
        var helpBlock          = $("#txtQuestionHelpBlock");
        var btnAskQuestionBack = $("#btnAskQuestionBack");
        var btnAskQuestionNext = $("#btnAskQuestionNext");
        var question           = "";
        var questionsEndpoint  = "/api/questions/";

        // Capture enter in Question textarea and submit
        txtQuestion.keydown(function(event) {
          if (event.keyCode == 13) {
            event.preventDefault();
            askQuestionForm.submit();
            return false;
          }
        });

        // Handle question form submission
        askQuestionForm.submit(function(event) {
          event.preventDefault();
          question = txtQuestion.val();

          if (question == "") {
            // No question has been entered
            askQuestionForm.addClass('has-error');
            helpBlock.text("Please enter a question");

          } else {
            // Disable the text area and the next button
            txtQuestion.attr('disabled', 'disabled');
            btnAskQuestionNext.attr('disabled',' disabled');

            // Submit to similar questions endpoint
            $.post(
              questionsEndpoint,
              {
                "text": question
              },
              onQuestionPostSuccess
            ).fail(onQuestionPostFailure);

          }

          return false;

        });

        function onQuestionPostSuccess(data) {
          if (data.page_url) {
            window.location.href = data.page_url;
          } else {
            console.log("Success!");
            askQuestionModal.modal("hide");
          }
        }

        function onQuestionPostFailure(jqXHR, textStatus, errorThrown) {
          reason = jqXHR.responseJSON.detail;
          askQuestionForm.addClass('has-error');
          helpBlock.text(reason);

          question = "";
          txtQuestion.val('');
          txtQuestion.removeAttr('disabled');
          btnAskQuestionNext.removeAttr('disabled');
        }

        // On modal close, reset the form back to original state
        askQuestionModal.on('hidden.bs.modal', function(event) {
          question = "";
          txtQuestion.val('');
          txtQuestion.removeAttr('disabled');
          helpBlock.text("");
          btnAskQuestionNext.removeAttr('disabled');
          btnAskQuestionBack.removeAttr('disabled');
          btnAskQuestionBack.addClass('invisible');
          askQuestionForm.removeClass('has-error');
        });

    });
})(jQuery);
