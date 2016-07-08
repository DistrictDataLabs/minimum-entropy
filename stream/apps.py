# stream.apps
# Describes the Stream application for Django
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Mar 04 23:25:07 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [70aac9d] benjamin@bengfort.com $

"""
Describes the Stream application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Freebase Config
##########################################################################

class StreamConfig(AppConfig):
    name = 'stream'
    verbose_name = "Activity Stream"
