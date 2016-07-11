# fugato.templatetags.paginator
# Provides a paginator tag context for digg-style pagination.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Jul 08 12:38:38 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: paginator.py [6f1c3bb] benjamin@bengfort.com $

"""
Provides a paginator tag context for digg-style pagination.

Based on: http://www.djangosnippets.org/snippets/73/

Modified by Sean Reifschneider to be smarter about surrounding page
link context.  For usage documentation see:

http://www.tummy.com/Community/Articles/django-pagination/
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

@register.inclusion_tag('components/pagination.html', takes_context=True)
def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """

    # Collect the pagination objects from the context
    page_obj = context['page_obj']
    paginator = context['paginator']

    # Determine the start page for the paginator
    startPage = max(page_obj.number - adjacent_pages, 1)
    if startPage <= 3: startPage = 1

    # Determine the end page for the paginatio
    endPage = page_obj.number + adjacent_pages + 1
    if endPage >= paginator.num_pages - 1: endPage = paginator.num_pages + 1

    # Create a list of page numbers to iterate over on the front end.
    page_numbers = [
        idx for idx in range(startPage, endPage)
        if idx > 0 and idx <= paginator.num_pages
    ]

    # Return a new context with the computed pagination ranges.
    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
    }
