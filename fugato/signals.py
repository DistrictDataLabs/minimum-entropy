# fugato.signals
# Signals for the fugato app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Mar 04 15:18:41 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals for the fugato app
"""

##########################################################################
## Imports
##########################################################################

from stream.signals import stream
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from django.conf import settings
from minent.utils import signature, nullable, htmlize
from fugato.models import Question, Answer

##########################################################################
## Question Signals
##########################################################################

@receiver(pre_save, sender=Question)
def question_normalization(sender, instance, *args, **kwargs):
    instance.hash = signature(instance.text)


@receiver(pre_save, sender=Question)
def question_render_markdown(sender, instance, *args, **kwargs):
    if instance.details == "":
        instance.details = None

    if instance.details is not None:
        instance.details_rendered = htmlize(instance.details)
    else:
        instance.details_rendered = None


@receiver(post_save, sender=Question)
def send_asked_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "asked" activity to the stream on Question create
    """
    if created:
        joined = {
            'sender':    sender,
            'actor':     instance.author,
            'verb':      'ask',
            'target':    instance,
            'timestamp': instance.created,
        }
        stream.send(**joined)

##########################################################################
## Answer Signals
##########################################################################

@receiver(pre_save, sender=Answer)
def answer_render_markdown(sender, instance, *args, **kwargs):
    if instance.text is not None:
        instance.text_rendered = htmlize(instance.text)


@receiver(post_save, sender=Answer)
def send_answered_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "answered" activity to the stream on Question create
    """
    if created:
        activity = {
            'sender':    sender,
            'actor':     instance.author,
            'verb':      'answer',
            'theme':     instance,
            'target':    instance.question,
            'timestamp': instance.created,
        }
        stream.send(**activity)
