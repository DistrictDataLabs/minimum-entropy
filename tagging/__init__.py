# tagging
# Provides a non-generic tagging methodology for minimum-entropy models.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jul 06 15:28:00 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Provides a non-generic tagging methodology for minimum-entropy models. Other
Django apps that allow for tagging use generics, but here I want to only tag
specific objects in specific ways, and separate the tags from the model that
they are associated with. 
"""

##########################################################################
## Configuration
##########################################################################

default_app_config = 'tagging.apps.TaggingConfig'
