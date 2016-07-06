# voting.templatetags.votable
# Tags for the Voting app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jan 27 11:59:19 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: votable.py [] benjamin@bengfort.com $

"""
Tags for the Voting app
"""

##########################################################################
## Imports
##########################################################################

from django import template
from voting.models import Vote
from django.contrib.contenttypes.models import ContentType

##########################################################################
## Module constants
##########################################################################

register = template.Library()

##########################################################################
## Assignment Tags
##########################################################################

@register.assignment_tag(takes_context=True)
def current_user_vote(context, content):
    """
    Returns the current user's vote for the given content:

        -1 is a downvote
         0 is a novote
         1 is an upvote

    Note that if the vote doesn't exist, a 0 is returned
    """

    kwargs = {
        'content_type': ContentType.objects.get_for_model(content),
        'object_id': content.id,
        'user': context['user'],
    }

    vote  = Vote.objects.filter(**kwargs).first()

    if vote is None:
        return 0
    else:
        return vote.vote
