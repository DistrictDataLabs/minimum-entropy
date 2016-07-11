# stream.admin
# Admin site configuration for activity stream
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 11 09:01:33 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [70aac9d] benjamin@bengfort.com $

"""
Admin site configuration for activity stream
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from stream.models import StreamItem

##########################################################################
## Register Admin
##########################################################################

# Stream Item is too complicated for the CMS without a custom interface.
# admin.site.register(StreamItem)
