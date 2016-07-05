# minent.settings.testing
# Testing settings to enable testing on Travis with Django tests.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 14:26:23 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: testing.py [] benjamin@bengfort.com $

"""
Testing settings to enable testing on Travis with Django tests.
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Test Settings
##########################################################################

## Debugging Settings
DEBUG            = True

## Hosts
ALLOWED_HOSTS    = ['localhost', '127.0.0.1']

## Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('DB_NAME', 'minent'),
        'USER': environ_setting('DB_USER', 'postgres'),
        'PASSWORD': environ_setting('DB_PASS', ''),
        'HOST': environ_setting('DB_HOST', 'localhost'),
        'PORT': environ_setting('DB_PORT', '5432'),
    },
}
