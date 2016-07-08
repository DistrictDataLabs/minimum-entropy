# voting.signals
# Signals handling for the Voting app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Mar 04 23:35:42 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals handling for the Voting app
"""

##########################################################################
## Imports
##########################################################################

from voting.models import Vote
from stream.signals import stream
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType


##########################################################################
## Signals
##########################################################################

@receiver(post_save, sender=Vote)
def send_voted_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "voted" activity to the stream on up/down vote

    Decisions:
        1. The vote object isn't included in the stream
        2. Activities are recorded even when votes are changed
        3. The target of the vote verb is the content_object
    """
    vote_verb = {
         1: 'upvote',
        -1: 'downvote',
         0:  None
    }[instance.vote]

    if vote_verb is None:
        return

    voted = {
        'sender':    sender,
        'actor':     instance.user,
        'verb':      vote_verb,
        'target':    instance.content_object,
    }
    stream.send(**voted)


@receiver(post_save, sender=Vote)
def update_answer_order_by_votes_signal(sender, instance, created, **kwargs):
    """
    Whenever a vote is saved, update the question's answer order with the new
    voting information and therefore the new voting order.
    """
    ctype = instance.content_type
    if ctype.app_label == 'fugato' and ctype.model == 'answer':
        # We have a vote for an answer! Set the answer order based on votes!
        instance.content_object.question.set_answer_order_by_votes()
