# minent.settings.production
# The Django settings for minimum-entropy in production
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 14:25:12 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: production.py [] benjamin@bengfort.com $

"""
The Django settings for minimum-entropy in production
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Production Settings
##########################################################################

## Debugging Settings
DEBUG            = False

## Hosts
ALLOWED_HOSTS    = ['ddl-minent.herokuapp.com', 'minent.districtdatalabs.com']

## Static files served by WhiteNoise
STATIC_ROOT = os.path.join(PROJECT, 'staticfiles')
