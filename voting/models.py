# voting.models
# ContentTypes based generic models for voting on anything!
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Jan 15 16:02:31 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [8eae6c4] benjamin@bengfort.com $

"""
ContentTypes based generic models for voting on anything!
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from voting.managers import VotingManager

##########################################################################
## Models
##########################################################################

class Vote(TimeStampedModel):
    """
    Generic vote object for up and down voting things
    """

    BALLOT   = Choices((-1, 'downvote', 'downvote'), (1, 'upvote', 'upvote'), (0, 'novote', 'novote'))

    # Data fields for the voting object
    vote     = models.SmallIntegerField( choices=BALLOT, default=BALLOT.novote )
    user     = models.ForeignKey( 'auth.User', related_name='votes' )

    # Content types for a generic relationship (e.g. vote anything)
    content_type   = models.ForeignKey( ContentType )
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey( 'content_type', 'object_id' )

    # Set a custom manager for the Vote object
    objects   = VotingManager()

    def __str__(self):
        action = {
            -1: "down voted",
            0:  "no voted",
            1:  "up voted",
        }[self.vote]

        return u"%s %s %s" % (unicode(self.user), action, unicode(self.content_object))

    class Meta:
        db_table = "voting"
        get_latest_by = "modified"
        verbose_name  = "vote"
        verbose_name_plural = "votes"
        unique_together = ('object_id', 'user', 'content_type')
