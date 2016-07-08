# tagging.managers
# Custom query methods for Tag objects and their relationships.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Jul 07 08:04:20 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: managers.py [c5d00aa] benjamin@bengfort.com $

"""
Custom query methods for Tag objects and their relationships.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from django.db.models.functions import Lower


##########################################################################
## Tag QuerySet
##########################################################################

class TagQuerySet(models.query.QuerySet):
    """
    Adds special methods to a query set of tags.
    """

    def to_csv(self):
        """
        Simple (naive) implementation of comma separated values of tags.
        """
        return ", ".join([tag.text for tag in self])

    def lexical_ordering(self):
        """
        Returns a case-insensitive lexical ordering of the tags.
        """
        return self.order_by(Lower('text'))


##########################################################################
## Tag Manager
##########################################################################

class TagManager(models.Manager):

    def tag(self, tag):
        """
        Looks up a tag by name (e.g. a helper method for get)
        """
        return self.get(text=tag)

    def to_csv(self):
        """
        QuerySet methods must be mirrored on the Manager.
        """
        return self.get_queryset().to_csv()

    def lexical_ordering(self):
        """
        Returns a case-insensitive lexical ordering of the tags.
        """
        return self.get_queryset().lexical_ordering()

    def get_queryset(self):
        """
        Return a TagQuerySet instead of the standard queryset.
        """
        return TagQuerySet(self.model, using=self._db)
