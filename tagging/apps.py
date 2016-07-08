# tagging.apps
# Describes the tagging application to Django
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jul 06 15:31:07 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [c5d00aa] benjamin@bengfort.com $

"""
Describes the tagging application to Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig


##########################################################################
## Fugato Config
##########################################################################

class TaggingConfig(AppConfig):

    name = 'tagging'

    def ready(self):
        import tagging.signals
