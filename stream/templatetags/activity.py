# stream.templatetags.activity
# Representations of activity stream objects.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jul 11 08:38:32 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: activity.py [001baf8] benjamin@bengfort.com $

"""
Representations of activity stream objects.
"""

##########################################################################
## Imports
##########################################################################

from django import template

##########################################################################
## Module Constants
##########################################################################

register = template.Library()


##########################################################################
## Inclusion Tags
##########################################################################

@register.inclusion_tag('stream/activities.html')
def activity_stream(user):
    return {
        'activity_stream': user.activity_stream.all()[:10],
    }


@register.inclusion_tag('stream/actor.html')
def actor_detail(activity):
    return {
        'actor': activity.actor,
        'repr': activity.get_object_repr(activity.actor),
    }

@register.inclusion_tag('stream/theme.html')
def theme_detail(activity):
    return {
        'theme': activity.theme,
        'href': activity.get_object_url(activity.theme),
        'repr': activity.get_object_repr(activity.theme),
        'content_type': activity.theme_content_type.name,
    }

@register.inclusion_tag('stream/target.html')
def target_detail(activity):
    return {
        'target': activity.target,
        'href': activity.get_object_url(activity.target),
        'repr': activity.get_object_repr(activity.target),
        'content_type': activity.target_content_type.name,
    }
