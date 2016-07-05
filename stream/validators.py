# stream.validators
# Custom validators for the activity stream
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Feb 04 11:41:24 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: validators.py [] benjamin@bengfort.com $

"""
Custom validators for the activity stream
"""

##########################################################################
## Imports
##########################################################################

from model_utils import Choices
from django.core.exceptions import ValidationError

##########################################################################
## Choices Validator
##########################################################################

class ChoiceValidator(object):
    """
    Validates a Django field to ensure that it is set as one of the choices
    """

    def __init__(self, choices):
        if not isinstance(choices, Choices):
            choices = Choices(choices)

        self.choices = choices

    def __call__(self, value):
        if value not in self.choices:
            raise ValidationError("%s is not one of the choices!" % value)
