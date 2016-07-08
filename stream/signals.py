# stream.signals
# Signal attachment for various models to activity stream
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Feb 04 12:20:10 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [70aac9d] benjamin@bengfort.com $

"""
Signal attachment for various models to activity stream

Proposed API for the activity stream:

    1. To use the activity stream: `from stream import stream`
    2. On post_save send the stream signal: stream.send(sender, **kwargs)
    3. Typically the sender will be the target, but might also be the actor
    4. The stream handler will capture the signal and create a new StreamActivity
"""

##########################################################################
## Imports
##########################################################################

from stream.models import StreamItem
from django.dispatch import Signal, receiver
from django.contrib.contenttypes.models import ContentType

##########################################################################
## Module Constants
##########################################################################

signal_args = (
    'actor', 'verb', 'theme', 'target', 'details', 'timestamp', 'public'
)

##########################################################################
## Stream Signal
##########################################################################

stream = Signal(providing_args=signal_args)

##########################################################################
## Stream Receiver
##########################################################################

@receiver(stream)
def stream_handler(sender, **kwargs):
    """
    The stream handler creates StreamItems from signals sent by the actors
    or targets that want to register their activity in the stream.
    """

    ## assertions for required arguments
    assert 'actor' in kwargs
    assert 'verb' in kwargs

    ## Create the keyword arguments for creating the activity stream
    activity = {
        'actor': kwargs.get('actor'),
        'verb': kwargs.get('verb'),
    }

    ## Other arguments (don't include if not present)
    for other in ('details', 'timestamp', 'public'):
        if other in kwargs:
            activity[other] = kwargs[other]

    ## Handle content types
    for generic in ('theme', 'target'):
        if generic in kwargs:
            ctypekey = '%s_content_type' % generic  # Create generic content_type attribute
            objidval = '%s_object_id' % generic     # Create generic object_id attribute
            content  = kwargs[generic]              # Get the generic content from the kwargs

            activity[ctypekey] = ContentType.objects.get_for_model(content)
            activity[objidval] = content.id

    ## Create the StreamItem
    StreamItem.objects.create(**activity)
