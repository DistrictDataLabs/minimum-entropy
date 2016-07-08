# voting.tests
# Tests for the voting module
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jan 27 08:49:03 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: tests.py [8eae6c4] benjamin@bengfort.com $

"""
Tests for the voting module
"""

##########################################################################
## Imports
##########################################################################

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import serializers

from fugato.models import *
from voting.models import *
from voting.serializers import *
from django.contrib.auth.models import User

from stream.signals import stream
from stream.models import StreamItem

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

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
    'question': {
        'text': 'Why did the chicken cross the road?',
        'author': None
    }
}

##########################################################################
## Serializer Tests
##########################################################################

class SerializerTests(APITestCase):
    """
    Test added functionality in voting serializers
    """

    def assertNotRaises(self, exc, fun, *args, **kwds):
        try:
            fun(*args, **kwds)
        except exc:
            self.fail("%s exception was raised", exc.__class__.__name__)

    def test_in_range_validator(self):
        """
        Test the in-range validator
        """

        validator = InRange(-1, 1)

        self.assertRaises(serializers.ValidationError, validator, -2)
        self.assertRaises(serializers.ValidationError, validator, 2)
        self.assertNotRaises(serializers.ValidationError, validator, -1)
        self.assertNotRaises(serializers.ValidationError, validator, 1)
        self.assertNotRaises(serializers.ValidationError, validator, 0)

    def test_voting_serializer_vote_range(self):
        """
        Ensure that the vote in the serializer is in range
        """

        serializer = VotingSerializer(data={"vote":-1})
        self.assertTrue(serializer.is_valid(), "downvote is not valid")

        serializer = VotingSerializer(data={"vote":0})
        self.assertTrue(serializer.is_valid(), "novote is not valid")

        serializer = VotingSerializer(data={"vote":1})
        self.assertTrue(serializer.is_valid(), "upvote is not valid")

        serializer = VotingSerializer(data={"vote":10})
        self.assertFalse(serializer.is_valid(), "bad vote is valid")

##########################################################################
## Model Tests
##########################################################################

class VotingModelTests(TestCase):
    """
    Test the Vote model/manager functionality
    """

    def setUp(self):
        self.user     = User.objects.create_user(**fixtures['user'])
        fixtures['question']['author'] = self.user
        self.question = Question.objects.create(**fixtures['question'])

    def test_punch_ballot(self):
        """
        Test the punch ballot method of the Vote manager
        """

        # Ensure that there are no votes for the question to start
        self.assertEqual(self.question.votes.count(), 0)
        self.assertEqual(Vote.objects.upvotes().count(), 0)
        self.assertEqual(Vote.objects.downvotes().count(), 0)

        vote, created = Vote.objects.punch_ballot(self.question, self.user, 1)
        self.assertTrue(created)
        self.assertEqual(self.question.votes.count(), 1)
        self.assertEqual(Vote.objects.upvotes().count(), 1)
        self.assertEqual(Vote.objects.downvotes().count(), 0)

        vote, created = Vote.objects.punch_ballot(self.question, self.user, -1)
        self.assertFalse(created)
        self.assertEqual(self.question.votes.count(), 1)
        self.assertEqual(Vote.objects.upvotes().count(), 0)
        self.assertEqual(Vote.objects.downvotes().count(), 1)

        vote, created = Vote.objects.punch_ballot(self.question, self.user)
        self.assertFalse(created)
        self.assertEqual(self.question.votes.count(), 1)
        self.assertEqual(Vote.objects.upvotes().count(), 0)
        self.assertEqual(Vote.objects.downvotes().count(), 0)

        self.assertEqual(Vote.objects.count(), 1)


    def test_punch_ballot_kwargs(self):
        """
        Ensure that punch ballot requires content and user
        """
        self.assertRaises(TypeError, Vote.objects.punch_ballot, content=self.question)
        self.assertRaises(TypeError, Vote.objects.punch_ballot, user=self.user)

    def test_upvote_send_stream(self):
        """
        Assert that 'upvote' stream signal is sent
        """
        handler = MagicMock()
        stream.connect(handler)
        vote, created = Vote.objects.punch_ballot(self.question, self.user, 1)

        # Ensure that the signal was sent once with required arguments
        handler.assert_called_once_with(verb='upvote', sender=Vote,
            actor=self.user, target=self.question, signal=stream)

    def test_downvote_send_stream(self):
        """
        Assert that 'downvote' stream signal is sent
        """
        handler = MagicMock()
        stream.connect(handler)
        vote, created = Vote.objects.punch_ballot(self.question, self.user, -1)

        # Ensure that the signal was sent once with required arguments
        handler.assert_called_once_with(verb='downvote', sender=Vote,
            actor=self.user, target=self.question, signal=stream)

    def test_voted_activity(self):
        """
        Assert that when a ballot is punched, there is an activity stream item
        """
        vote, created = Vote.objects.punch_ballot(self.question, self.user, 1)
        target_content_type = ContentType.objects.get_for_model(self.question)
        target_object_id    =  self.question.id

        query = StreamItem.objects.filter(verb='upvote', actor=self.user,
                    target_content_type=target_content_type, target_object_id=target_object_id)

        self.assertEqual(query.count(), 1, "no stream item created!")
