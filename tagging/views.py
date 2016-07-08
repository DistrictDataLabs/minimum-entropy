# tagging.views
# Views for the tagging module.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Jul 08 15:55:09 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the tagging module.
"""

##########################################################################
## Imports
##########################################################################

from tagging.models import Tag
from users.mixins import LoginRequired
from django.views.generic import ListView


##########################################################################
## HTML Generating Views
##########################################################################

class TagList(LoginRequired, ListView):
    """
    Authenticated web application view that lists the tags in a paginated
    fashion. This view supports a view of the tags as a grid in particular.
    """

    model = Tag
    template_name = "tagging/list.html"
    context_object_name = "tag_list"
    paginate_by = 16

    def get_queryset(self):
        """
        Peforms tag ordering of the queryset and can be adapted to support
        filtering or search based on the query arguments.
        """
        # Right now just return alphabetical ordering
        queryset = super(TagList, self).get_queryset()
        return queryset.lexical_ordering()

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)

        # Add rendering params for the view
        context['navbar_active'] = "tags"

        # TODO: This might be very slow, improve this!
        context['num_all_tags'] = self.model.objects.count()

        return context
