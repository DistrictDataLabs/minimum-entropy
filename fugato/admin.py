# fugato.admin
# Description of the app for the admin site and CMS.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 20:04:50 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Description of the app for the admin site and CMS.
"""

##########################################################################
## Imports
##########################################################################


from django.contrib import admin
from fugato.models import Question, Answer

##########################################################################
## Register Models
##########################################################################

admin.site.register(Question)
admin.site.register(Answer)
