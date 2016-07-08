# tagging.serializers
# Serialization for the REST API endpoints for tags.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Jul 07 19:18:03 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: serializers.py [6eb4b7c] benjamin@bengfort.com $

"""
Serialization for the REST API endpoints for tags.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import serializers

##########################################################################
## CSV Field
##########################################################################

class CSVField(serializers.CharField):
    """
    Handles the serialization and deserialization of CSV data.
    """

    def to_representation(self, obj):
        """
        If the object is already a string, return that - otherwise join the
        iterable with a comma and a space for csv serialization.

        NOTE: Does not escape quotes or commas.
        """
        if isinstance(obj, str):
            return obj
        else:
            return ", ".join(obj)

    def to_internal_value(self, data):
        """
        Parses a CSV value to a list, filtering empty strings.
        """
        return list(filter(None, [
            text.strip() for text in data.split(",")
        ]))

##########################################################################
## Validators
##########################################################################

class MaxLength(object):
    """
    Validator that specifies a value must have a length smaller than given.
    """

    def __init__(self, limit, things="items"):
        self.limit  = limit
        self.things = things

    def __call__(self, value):
        if len(value) > self.limit:
            raise serializers.ValidationError(
                "Cannot add more than {} {}!".format(self.limit, self.things)
            )



##########################################################################
## Serializers
##########################################################################

class CSVTagSerializer(serializers.Serializer):
    """
    Deserializes a JSON request containing CSV tagged data.
    """

    @staticmethod
    def serialize_question(question):
        """
        Returns a dictionary of serialized data from the question object.
        """
        return {
            'tags': [tag.text for tag in question.tags.all()],
            'csv_tags': question.tags.all().to_csv(),
        }


    ## CSV Fields
    csv_tags = CSVField(validators=[MaxLength(limit=5, things="tags")])
    tags     = serializers.ListField(child=serializers.CharField(), read_only=True)
