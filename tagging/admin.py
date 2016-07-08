# tagging.admin
# Registration of tag model management for Django Admin CMS
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Jul 07 17:02:44 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [c5d00aa] benjamin@bengfort.com $

"""
Registration of tag model management for Django Admin CMS
"""

##########################################################################
## Imports
##########################################################################

from tagging.models import Tag
from django.contrib import admin


##########################################################################
## Admin Registration
##########################################################################

admin.site.register(Tag)
