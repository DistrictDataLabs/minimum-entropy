# tagging.managers
# Custom query methods for Tag objects and their relationships.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Jul 07 08:04:20 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Custom query methods for Tag objects and their relationships.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models


##########################################################################
## Tag Manager
##########################################################################

class TagManager(models.Manager):

    def tag(self, tag):
        """
        Looks up a tag by name (e.g. a helper method for get)
        """
        return self.get(text=tag)
