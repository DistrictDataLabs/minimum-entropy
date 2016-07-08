# tagging.models
# Models for the tagging app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jul 06 15:34:02 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [c5d00aa] benjamin@bengfort.com $

"""
Models for the tagging app
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from minent.utils import nullable, notnullable
from tagging.managers import TagManager

##########################################################################
## Question Tags
##########################################################################

class Tag(TimeStampedModel):

    text        = models.CharField(max_length=100, unique=True)
    slug        = AutoSlugField(populate_from='text', unique=True)
    description = models.CharField(max_length=255, **nullable)
    creator     = models.ForeignKey('auth.User', related_name='tags')
    is_synonym  = models.BooleanField(default=False)
    head_word   = models.ForeignKey('self', related_name='synonyms', **nullable)

    ## Set custom tag manager
    objects     = TagManager()

    class Meta:
        db_table = "tags"
        get_latest_by = "created"

    def __str__(self):
        return self.text
