# users.signals
# Signals management for the Users app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Mar 04 23:30:27 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals management for the Users app
"""

##########################################################################
## Imports
##########################################################################

import hashlib

from minent.utils import htmlize
from stream.signals import stream
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from users.models import Profile
from django.contrib.auth.models import User

##########################################################################
## Signals
##########################################################################

@receiver(pre_save, sender=Profile)
def question_render_markdown(sender, instance, *args, **kwargs):
    if instance.biography:
        instance.biography_rendered = htmlize(instance.biography)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile object for the user if it doesn't exist, or updates
    it with new information from the User (e.g. the gravatar).
    """
    ## Compute the email hash
    digest = hashlib.md5(instance.email.lower().encode("utf-8")).hexdigest()

    if created:
        Profile.objects.create(user=instance, email_hash=digest)
    else:
        instance.profile.email_hash = digest
        instance.profile.save()


@receiver(post_save, sender=User)
def send_joined_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "joined" activity to the stream on create
    """
    if created:
        joined = {
            'sender':    sender,
            'actor':     instance,
            'verb':      'join',
            'timestamp': instance.date_joined,
        }
        stream.send(**joined)
