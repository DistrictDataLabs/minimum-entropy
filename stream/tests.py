# stream.tests
# Testing the Activity Stream library
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Feb 04 11:18:38 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Testing the Activity Stream library
"""

##########################################################################
## Imports
##########################################################################

from unittest import skip
from django.test import TestCase
from stream.models import *
from fugato.models import *
from voting.models import *
from django.contrib.auth.models import User
from django.utils import timezone as datetime
from datetime import timedelta

##########################################################################
## Fixtures
##########################################################################

fixtures = {
    'user': {
        'username': 'jdoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'jdoe@example.com',
        'password': 'supersecret',
    },
    'voter' : {
        'username': 'bobbyd',
        'first_name': 'Bob',
        'last_name': 'Dylan',
        'email': 'bobby@example.com',
        'password': 'dontguessthis',
    },
    'question': {
        'text': 'Why is the sky blue?',
        'author': None
    },
    'annotation': {
        'text': 'sky',
        'question': None,
        'user': None,
    }
}

##########################################################################
## Stream Model Tests
##########################################################################

class StreamItemModelTest(TestCase):

    def setUp(self):
        self.user     = User.objects.create_user(**fixtures['user'])
        self.voter    = User.objects.create_user(**fixtures['voter'])

        fixtures['question']['author'] = self.user
        self.question = Question.objects.create(**fixtures['question'])

        fixtures['annotation']['user'] = self.user
        fixtures['annotation']['question'] = self.question

    def one_minute_ago(self):
        """
        Helper function to return a datetime one minute ago
        """
        return datetime.now() - timedelta(minutes=1)

    @skip("pending implementation")
    def test_user_feed(self):
        """
        Check that a user's feed is accessible
        """
        pass

    @skip("pending implementation")
    def test_user_feed_privacy(self):
        """
        Assert that a user's public only feed is accessible
        """
        pass

    @skip("pending implementation")
    def test_no_empty_verb(self):
        """
        Ensure that no empty verb can be added to the database
        """
        pass

    def test_actor_verb(self):
        """
        Test a StreamItem with only an actor and a verb
        """

        event = StreamItem.objects.create(**{
                'actor': self.user,
                'verb': StreamItem.VERBS.join,
                'timestamp': self.one_minute_ago(),
            })

        expected = u'jdoe joined 1 minute ago'

        self.assertEqual(str(event), expected)

    def test_actor_verb_target(self):
        """
        Test a StreamItem with an actor, verb, and target
        """

        event = StreamItem.objects.create(**{
                'actor': self.user,
                'verb': StreamItem.VERBS.ask,
                'target': self.question,
                'timestamp': self.one_minute_ago(),
            })

        expected = u'jdoe asked Why is the sky blue? 1 minute ago'

        self.assertEqual(str(event), expected)

    def test_actor_verb_theme(self):
        """
        Test a StreamItem with an actor, verb, and theme
        """

        event = StreamItem.objects.create(**{
                'actor': self.user,
                'verb': StreamItem.VERBS.upvote,
                'theme': self.question,
                'timestamp': self.one_minute_ago(),
            })

        expected = u'jdoe up voted Why is the sky blue? 1 minute ago'

        self.assertEqual(str(event), expected)

    @skip("annotation doesn't exist in minimum-entropy")
    def test_actor_verb_target_theme(self):
        """
        Test a StreamItem with an actor, verb, theme and target
        """

        event = StreamItem.objects.create(**{
                'actor': self.user,
                'verb': StreamItem.VERBS.annotate,
                'target': self.question,
                'theme': self.annotation,
                'timestamp': self.one_minute_ago(),
            })

        expected = u'jdoe annotated sky on Why is the sky blue? 1 minute ago'

        self.assertEqual(str(event), expected)
