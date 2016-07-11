# stream.models
# Database models for the Activity Stream Items
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Feb 04 10:24:36 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [70aac9d] benjamin@bengfort.com $

"""
Database models for the Activity Stream items
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from model_utils import Choices
from django.utils.timesince import timesince
from minent.utils import nullable, notnullable
from stream.managers import StreamItemManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone as datetime

##########################################################################
## Activity Stream models
##########################################################################

class StreamItem(models.Model):
    """
    Contains a relationship between a user and any other content item via
    a Generic relationship. It can then be used to describe an action
    model as follows:

        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <theme> <target> <time>

    For example:

        <bbengfort> <logged in> <1 minute ago>
        <mcox> <asked> <question> <2 hours ago>
        <dperlis> <annotated> <topic> on <question> <a day ago>

    Much of this data type is created automatically (e.g. not interacted
    with by users except through views). A secondary table is used to
    store the activity stream to ensure that it can be quickly loaded,
    even though many of the items in question already have a relationship
    to some user!
    """

    ## Potential actions (verbs) for the activity stream
    ## DB storage is the infinitive, display is past tense
    VERBS = Choices(
            ('join', 'joined'),
            ('view', 'viewed'),
            ('upvote', 'up voted'),
            ('downvote', 'down voted'),
            ('ask', 'asked'),
            ('answer', 'answered'),
        )

    ## Relationship to the user (the actor)
    actor     = models.ForeignKey( 'auth.User', related_name='activity_stream' ) # The actor causing the event

    ## Generic relationship to a target
    target_content_type = models.ForeignKey( ContentType, related_name="targets", **nullable )
    target_object_id    = models.PositiveIntegerField( **nullable )
    target              = GenericForeignKey( 'target_content_type', 'target_object_id' )

    ## Generic relationship to a theme (action object)
    theme_content_type  = models.ForeignKey( ContentType, related_name="themes", **nullable )
    theme_object_id     = models.PositiveIntegerField( **nullable )
    theme               = GenericForeignKey( 'theme_content_type', 'theme_object_id' )

    ## Meta data concerning the activity
    public    = models.BooleanField( default=True )                              # May appear in public feeds?
    verb      = models.CharField( max_length=20, choices=VERBS )                 # The "verb" or "action" or "event"
    details   = models.TextField( **nullable )                                   # Additional details about the action
    timestamp = models.DateTimeField( default=datetime.now, db_index=True )      # The timestamp of the action (note no created and modified)

    ## A custom manager for the StreamItem
    objects   = StreamItemManager()

    ## Database setup and meta
    class Meta:
        app_label = 'stream'
        db_table  = 'activity_stream'
        ordering  = ('-timestamp',)
        verbose_name = 'activity stream item'
        verbose_name_plural = 'activity stream items'

    ######################################################################
    ## Methods on the Stream Item
    ######################################################################

    def timesince(self, now=None):
        """
        Returns a string representation of the time since the timestamp.
        """
        return timesince(self.timestamp, now).encode('utf8').replace(b'\xc2\xa0', b' ').decode('utf8')

    def get_object_url(self, obj):
        """
        Returns the URL of an object by using the `get_absolute_url` method
        otherwise returns None. (Shouldn't raise an error).
        """
        if hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()
        return None

    def get_actor_url(self):
        return self.get_object_url(self.actor)

    def get_target_url(self):
        return self.get_object_url(self.target)

    def get_theme_url(self):
        return self.get_absolute_url(self.theme)

    def get_object_repr(self, obj):
        """
        Returns an HTML representation of an object, basically an anchor
        to the object's absolute URL or just the plain string representation.
        """

        # If the object knowns how to represent itself ...
        if hasattr(obj, 'get_stream_repr'):
            return obj.get_stream_repr()

        # Otherwise, simply return the string representation
        return str(obj)

    def __str__(self):
        context = {
            'actor': self.actor.username,
            'verb': self.get_verb_display(),
            'theme': self.get_object_repr(self.theme),
            'target': self.get_object_repr(self.target),
            'timesince': self.timesince(),
        }

        if self.target:
            if self.theme:
                return "{actor} {verb} {theme} on {target} {timesince} ago".format(**context)
            return "{actor} {verb} {target} {timesince} ago".format(**context)

        if self.theme:
            return "{actor} {verb} {theme} {timesince} ago".format(**context)

        return "{actor} {verb} {timesince} ago".format(**context)
