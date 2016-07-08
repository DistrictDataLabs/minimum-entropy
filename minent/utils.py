# minent.utils
# Project level utilities
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Oct 23 14:09:04 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: utils.py [] benjamin@bengfort.com $

"""
Project level utilities
"""

##########################################################################
## Imports
##########################################################################

import re
import time
import base64
import bleach
import hashlib

from functools import wraps
from markdown import markdown
from dateutil.relativedelta import relativedelta

##########################################################################
## Utilities
##########################################################################

## Nullable kwargs for models
nullable = { 'blank': True, 'null': True, 'default':None }

## Not nullable kwargs for models
notnullable = { 'blank': False, 'null': False }

##########################################################################
## Helper functions
##########################################################################

def normalize(text):
    """
    Normalizes the text by removing all punctuation and spaces as well as
    making the string completely lowercase.
    """
    return re.sub(r'[^a-z0-9]+', '', text.lower())


def signature(text):
    """
    This helper method normalizes text and takes the SHA1 hash of it,
    returning the base64 encoded result. The normalization method includes
    the removal of punctuation and white space as well as making the case
    completely lowercase. These signatures will help us discover textual
    similarities between questions.
    """
    text = normalize(text).encode('utf-8')
    return base64.b64encode(hashlib.sha1(text).digest())


def htmlize(text):
    """
    This helper method renders Markdown then uses Bleach to sanitize it as
    well as convert all links to actual links.
    """
    text = bleach.clean(text, strip=True)    # Clean the text by stripping bad HTML tags
    text = markdown(text)                    # Convert the markdown to HTML
    text = bleach.linkify(text)              # Add links from the text and add nofollow to existing links

    return text


# Compile regular expression functions for query normalization
find_terms = re.compile(r'"([^"]+)"|(\S+)').findall
norm_space = re.compile(r'\s{2,}').sub

def normalize_query(terms):
    """
    Splits the query string in individual keywords, getting rid of extra
    spaces and grouping quoted words together.

    Example:

        >>> normalize_query(' some random  words "with   quotes " and spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    return [
        norm_space(' ', (t[0] or t[1]).strip())
        for t in find_terms(terms)
    ]

##########################################################################
## Memoization
##########################################################################

def memoized(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent
    accesses is returned, preventing the need to call the getter any more.

    https://github.com/estebistec/python-memoized-property
    """
    attr_name = '_{0}'.format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)


##########################################################################
## Timer functions
##########################################################################

class Timer(object):
    """
    A context object timer. Usage:
        >>> with Timer() as timer:
        ...     do_something()
        >>> print timer.interval
    """

    def __init__(self, wall_clock=True):
        """
        If wall_clock is True then use time.time() to get the number of
        actually elapsed seconds. If wall_clock is False, use time.clock to
        get the process time instead.
        """
        self.wall_clock = wall_clock
        self.time = time.time if wall_clock else time.clock

    def __enter__(self):
        self.start    = self.time()
        return self

    def __exit__(self, type, value, tb):
        self.finish   = self.time()
        self.interval = self.finish - self.start

    def __str__(self):
        return humanizedelta(seconds=self.interval)


def timeit(func, wall_clock=True):
    """
    Returns the number of seconds that a function took along with the result
    """
    @wraps(func)
    def timer_wrapper(*args, **kwargs):
        """
        Inner function that uses the Timer context object
        """
        with Timer(wall_clock) as timer:
            result = func(*args, **kwargs)

        return result, timer
    return timer_wrapper


def humanizedelta(*args, **kwargs):
    """
    Wrapper around dateutil.relativedelta (same construtor args) and returns
    a humanized string representing the detla in a meaningful way.
    """
    delta = relativedelta(*args, **kwargs)
    attrs = ('years', 'months', 'days', 'hours', 'minutes', 'seconds')
    parts = [
        '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
        for attr in attrs if getattr(delta, attr)
    ]

    return " ".join(parts)
