# fugato.managers
# Custom managers for the fugato models
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jul 22 14:03:52 2015 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: managers.py [8eae6c4] benjamin@bengfort.com $

"""
Custom managers for the fugato models
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from minent.utils import signature, normalize_query
from django.db.models.functions import Coalesce

##########################################################################
## Tag QuerySet
##########################################################################

class QuestionQuerySet(models.query.QuerySet):
    """
    Adds special methods to a query set of question objects.
    """

    def unanswered(self):
        """
        Returns any question that is unanswered
        """
        return self.count_answers().filter(num_answers=0)

    def count_votes(self):
        """
        Returns questions annotated with the number of votes they have.
        """
        return self.annotate(num_votes=Coalesce(models.Sum('votes__vote'), 0))

    def count_answers(self):
        """
        Returns questions annotated with the number of answers they have.
        """
        return self.annotate(num_answers=models.Count('answers'))

    def search(self, terms):
        """
        Produces an icontains lookup on the question title.
        """
        query = None # Query to search for every search term

        # Build the query with Q and icontains
        for term in normalize_query(terms):
            q = models.Q(text__icontains=term) | models.Q(details__icontains=term)
            query = q if query is None else query & q

        return self.filter(query)


##########################################################################
## Questions Manager
##########################################################################

class QuestionManager(models.Manager):

    def dedupe(self, raise_for_exceptions=False, **kwargs):
        """
        Essentially a GET or CREATE method that checks if a duplicate
        question already exists in the database by its signature. If
        raise_for_exceptions is True, then will raise a DuplicateQuestion
        exception, otherwise it will return None.

        Returns question, created where created is a Boolean
        """
        qsig = signature(kwargs['text'])
        query = self.filter(signature=qsig)
        if query.exists():
            if raise_for_exceptions:
                raise DuplicateQuestion()
            return query.first(), False

        return self.create(**kwargs), True

    def unanswered(self):
        """
        Returns any question that is unanswered
        """
        return self.get_queryset().unanswered()

    def count_votes(self):
        """
        Returns questions annotated with the number of votes they have.
        """
        return self.get_queryset().count_votes()

    def count_answers(self):
        """
        Returns questions annotated with the number of answers they have.
        """
        return self.get_queryset().count_answers()

    def search(self, terms):
        """
        Produces an icontains lookup on the question title.
        """
        return self.get_queryset().search(terms)

    def get_queryset(self):
        """
        Return a QuestionQuerySet instead of the standard queryset.
        """
        return QuestionQuerySet(self.model, using=self._db)
