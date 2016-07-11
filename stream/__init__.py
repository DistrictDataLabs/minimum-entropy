# stream
# An app that implements an Activity Stream for minimum-entropy
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Feb 04 10:21:07 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: __init__.py [70aac9d] benjamin@bengfort.com $

"""
An app that implements an Activity Stream for minimum-entropy.

Activity Streams (or newsfeeds) are user specific events on a system. They
are becoming more popular, and even have a W3C specification!

See http://www.w3.org/TR/2014/WD-activitystreams-core-20141023/
"""

##########################################################################
## Configuration
##########################################################################

default_app_config = 'stream.apps.StreamConfig'
