# minent.wsgi
# WSGI Config for Minimum Entropy project
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 13:28:48 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: wsgi.py [916a654] benjamin@bengfort.com $

"""
WSGI config for minent project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

##########################################################################
## Imports
##########################################################################

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


##########################################################################
## Configuration
##########################################################################

## Load settings from environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minent.settings.production")

## Create Whitenoise application
application = get_wsgi_application()
application = DjangoWhiteNoise(application)
