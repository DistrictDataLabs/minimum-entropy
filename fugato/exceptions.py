# fugato.exceptions
# Custom exceptions for API
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jan 21 14:59:27 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: exceptions.py [] benjamin@bengfort.com $

"""
Custom exceptions for API
"""

##########################################################################
## Imports
##########################################################################

from rest_framework.exceptions import APIException

##########################################################################
## API Exceptions
##########################################################################

class DuplicateQuestion(APIException):

    status_code = 400
    default_detail = "question has already been asked"
