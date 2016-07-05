# minent.settings.development
# The Django settings for minimum-entropy in development.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 14:20:28 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: development.py [] benjamin@bengfort.com $

"""
The Django settings for minimum-entropy in development.
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Development Settings
##########################################################################

## Debugging Settings
DEBUG            = True

## Hosts
ALLOWED_HOSTS    = ('127.0.0.1', 'localhost')

## Content
MEDIA_ROOT       = os.path.join(PROJECT, 'media')
STATIC_ROOT      = 'staticfiles'
