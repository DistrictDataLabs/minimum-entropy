# voting.managers
# Custom manager model for voting objects
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jan 20 12:42:19 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Custom manager model for voting objects
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from django.contrib.contenttypes.models import ContentType

##########################################################################
## Voting Manager
##########################################################################

class VotingManager(models.Manager):

    def upvotes(self):
        """
        Return only the upvoted
        """
        return self.filter(vote=self.model.BALLOT.upvote)

    def downvotes(self):
        """
        Return only the down votes
        """
        return self.filter(vote=self.model.BALLOT.downvote)

    def punch_ballot(self, content=None, user=None, vote=0):
        """
        Essentially `update_or_create` with ContentType lookup
        """
        if content is None or user is None:
            raise TypeError("content and user are required for punch ballot")

        kwargs = {
            'content_type': ContentType.objects.get_for_model(content),
            'object_id': content.id,
            'user': user,
            'defaults': {
                'vote': vote,
            }
        }

        return self.update_or_create(**kwargs)
