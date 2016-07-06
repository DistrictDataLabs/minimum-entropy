# voting.serializers
# API Serializers for the voting module
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jan 27 08:38:52 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
API Serializers for the voting module
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import serializers

##########################################################################
## Validators
##########################################################################

class InRange(object):
    """
    Validator that specifies a value must be in a particular range
    """

    def __init__(self, low, high):
        self.low  = low
        self.high = high

    def __call__(self, value):
        if value > self.high or value < self.low:
            raise serializers.ValidationError("value must be between %d and %d (inclusive)" % (self.low, self.high))

##########################################################################
## Serializers
##########################################################################

class VotingSerializer(serializers.Serializer):
    """
    Serializes incoming votes.

    Note: There is no model associated with this serializer
    """

    vote    = serializers.IntegerField(validators=[InRange(-1,1)])
    display = serializers.SerializerMethodField('get_vote_display')

    def get_vote_display(self, obj):
        displays = {
            -1: "downvote",
             0: "novote",
             1: "upvote",
        }

        return displays[obj['vote']]
