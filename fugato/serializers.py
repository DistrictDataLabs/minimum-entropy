# fugato.serializers
# JSON Serializers for the Fugato app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 23 15:03:36 2014 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
JSON Serializers for the Fugato app
"""

##########################################################################
## Imports
##########################################################################

from fugato.models import *
from fugato.exceptions import *
from users.serializers import *

from minent.utils import signature
from rest_framework import serializers

##########################################################################
## Question Serializers
##########################################################################

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the Question object for use in the API.
    """

    author   = UserSerializer(
                default=serializers.CurrentUserDefault(),
                read_only=True,
               )

    page_url = serializers.SerializerMethodField()

    class Meta:
        model  = Question
        fields = ('url', 'text', 'author', 'page_url', 'details', 'details_rendered')
        extra_kwargs = {
            'url': {'view_name': 'api:question-detail',},
            'details_rendered': {'read_only': True},
        }

    ######################################################################
    ## Serializer Methods
    ######################################################################

    def get_page_url(self, obj):
        """
        Returns the models' detail absolute url.
        """
        return obj.get_absolute_url()

    #####################################################################
    ## Override create and update for API
    ######################################################################

    def create(self, validated_data):
        """
        Override the create method to deal with duplicate questions and
        other API-specific errors that can happen on Question creation.
        """

        ## Check to make sure there is no duplicate
        qsig = signature(validated_data['text'])
        if Question.objects.filter(signature=qsig).exists():
            raise DuplicateQuestion()

        ## Create the model as before
        return super(QuestionSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """
        Override the update method to perform non-duplication checks that
        aren't instance-specific and to determine if other fields should
        be updated like the parse or the concepts.

        Currently this is simply the default behavior.

        TODO:
            - Check if reparsing needs to be performed
            - Check if concepts need to be dealt with
            - Check if the question text has changed and what to do
        """
        return super(QuestionSerializer, self).update(instance, validated_data)


##########################################################################
## Answer Serializers
##########################################################################

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the Answer object for use in the API.
    """

    author   = UserSerializer(
                default=serializers.CurrentUserDefault(),
                read_only=True,
               )

    class Meta:
        model  = Answer
        fields = ('url', 'text', 'text_rendered', 'author', 'question', 'created', 'modified')
        read_only_fields = ('text_rendered', 'author')
        extra_kwargs = {
            'url': {'view_name': 'api:answer-detail',},
            'question': {'view_name': 'api:question-detail',}
        }
