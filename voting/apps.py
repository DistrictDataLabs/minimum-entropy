# voting.apps
# Describes the Voting application for Django
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Mar 04 23:34:16 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [8eae6c4] benjamin@bengfort.com $

"""
Describes the Voting application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Voting Config
##########################################################################

class VotingConfig(AppConfig):
    name = 'voting'
    verbose_name = "Voting"

    def ready(self):
        import voting.signals
