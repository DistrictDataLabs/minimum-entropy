# fugato.tests
# Tests the fugato app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Jan 23 07:27:20 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: tests.py [8eae6c4] benjamin@bengfort.com $

"""
Tests the fugato app
"""

##########################################################################
## Imports
##########################################################################

from unittest import skip
from fugato.models import *
from voting.models import *
from stream.signals import stream
from stream.models import StreamItem
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from urllib.parse import urlsplit
from django.contrib.contenttypes.models import ContentType

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
    'voter' : {
        'username': 'bobbyd',
        'first_name': 'Bob',
        'last_name': 'Dylan',
        'email': 'bobby@example.com',
        'password': 'dontguessthis',
    },
    'question': {
        'text': 'Why did the chicken cross the road?',
        'author': None
    },
    'answer': {
        'question': None,
        'author': None,
        'text': 'To get to the other side.',
    }
}

##########################################################################
## Fugato models tests
##########################################################################

class QuestionModelTest(TestCase):

    def setUp(self):
        self.user   = User.objects.create_user(**fixtures['user'])
        fixtures['question']['author'] = self.user

    def test_question_ask_send_stream(self):
        """
        Assert that when a question is created it sends the "ask" stream signal
        """
        handler = MagicMock()
        stream.connect(handler)
        question = Question.objects.create(**fixtures['question'])

        # Ensure that the signal was sent once with required arguments
        handler.assert_called_once_with(verb='ask', sender=Question,
                    timestamp=question.created, actor=self.user,
                    target=question, signal=stream)

    def test_question_asked_activity(self):
        """
        Assert that when a question is asked, there is an activity stream item
        """
        question = Question.objects.create(**fixtures['question'])
        target_content_type = ContentType.objects.get_for_model(question)
        target_object_id    =  question.id

        query = StreamItem.objects.filter(verb='ask', actor=self.user,
                    target_content_type=target_content_type, target_object_id=target_object_id)
        self.assertEqual(query.count(), 1, "no stream item created!")

class AnswerModelTest(TestCase):

    def setUp(self):
        self.user     = User.objects.create_user(**fixtures['user'])
        fixtures['question']['author'] = self.user
        fixtures['answer']['author'] = self.user

        self.question = Question.objects.create(**fixtures['question'])
        fixtures['answer']['question'] = self.question

    def test_question_answer_send_stream(self):
        """
        Assert that when an Answer is created it sends the "answer" stream signal
        """
        handler = MagicMock()
        stream.connect(handler)
        answer  = Answer.objects.create(**fixtures['answer'])

        # Ensure that the signal was sent once with required arguments
        handler.assert_called_once_with(verb='answer', sender=Answer,
                    timestamp=answer.created, actor=self.user, theme=answer,
                    target=self.question, signal=stream)

    def test_question_answered_activity(self):
        """
        Assert that when a question is answered, there is an activity stream item
        """
        answer  = Answer.objects.create(**fixtures['answer'])
        target_content_type = ContentType.objects.get_for_model(answer.question)
        target_object_id    =  answer.question.id
        theme_content_type  = ContentType.objects.get_for_model(answer)
        theme_object_id     = answer.id

        query   = {
            'verb': 'answer',
            'actor': self.user,
            'target_content_type': target_content_type,
            'target_object_id': target_object_id,
            'theme_content_type': theme_content_type,
            'theme_object_id': theme_object_id,
        }

        query = StreamItem.objects.filter(**query)
        self.assertEqual(query.count(), 1, "no stream item created!")


##########################################################################
## Fugato API Views tests
##########################################################################

class QuestionAPIViewSetTest(TestCase):

    def setUp(self):
        self.user   = User.objects.create_user(**fixtures['user'])
        fixtures['question']['author'] = self.user
        self.client = APIClient()

    def login(self):
        credentials = {
            'username': fixtures['user']['username'],
            'password': fixtures['user']['password'],
        }

        return self.client.login(**credentials)

    def logout(self):
        return self.client.logout();

    def test_question_list_auth(self):
        """
        Assert GET /api/question/ returns 403 when not logged in
        """
        endpoint = reverse('api:question-list')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_create_auth(self):
        """
        Assert POST /api/question/ returns 403 when not logged in
        """
        endpoint = reverse('api:question-list')
        response = self.client.post(endpoint, {'text': 'Where are my keys?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_retrieve_auth(self):
        """
        Assert GET /api/question/:id/ returns 403 when not logged in
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_update_auth(self):
        """
        Assert PUT /api/question/:id/ returns 403 when not logged in
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.put(endpoint, {'text': 'Why did the bear cross the road?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_delete_auth(self):
        """
        Assert DELETE /api/question/:id/ returns 403 when not logged in
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_vote_post_auth(self):
        """
        Assert POST /api/question/:id/vote returns 403 when not logged in
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url() + "vote/"

        response = self.client.post(endpoint, {'vote': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_answers_list_auth(self):
        """
        Assert GET /api/question/:id/answers returns 403 when not logged in
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url() + "answers/"

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_vote_get_auth(self):
        """
        Assert GET /api/question/:id/vote returns a 400
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url() + "vote/"

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login()

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @skip("pending implementation")
    def test_question_list(self):
        """
        Test GET /api/question/ returns question list
        """
        self.login()

        endpoint = reverse('api:question-list')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @skip("pending implementation")
    def test_question_create(self):
        """
        Test POST /api/question/ creates a question
        """
        self.login()

        endpoint = reverse('api:question-list')
        response = self.client.post(endpoint, {'text': 'Where are my keys?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @skip("pending implementation")
    def test_question_retrieve(self):
        """
        Test GET /api/question/:id/ returns a question detail
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @skip("pending implementation")
    def test_question_update(self):
        """
        Test PUT /api/question/:id/ updates a question
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.put(endpoint, {'text': 'Why did the bear cross the road?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_delete_auth(self):
        """
        Test DELETE /api/question/:id/ deletes a question
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(Question.objects.filter(pk=question.pk).exists())

    def test_question_create_vote(self):
        """
        Assert POST /api/question/:id/vote creates a vote for a user
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url() + "vote/"

        self.assertEqual(question.votes.count(), 0)

        response = self.client.post(endpoint, {'vote': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {'created': True, 'status': 'vote recorded', 'display': 'upvote'}
        self.assertDictContainsSubset(expected, response.data)

        self.assertEqual(question.votes.count(), 1)

    def test_question_update_vote(self):
        """
        Assert POST /api/question/:id/vote updates if already voted
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        vote, _  = Vote.objects.punch_ballot(content=question, user=self.user, vote=1)
        endpoint = question.get_api_detail_url() + "vote/"

        self.assertEqual(question.votes.count(), 1)

        response = self.client.post(endpoint, {'vote': -1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {'created': False, 'status': 'vote recorded', 'display': 'downvote'}
        self.assertDictContainsSubset(expected, response.data)

        self.assertEqual(question.votes.count(), 1)

    def test_question_vote_response(self):
        """
        Ensure POST /api/question/:id/vote response contains expected data
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url() + "vote/"

        self.assertEqual(question.votes.count(), 0)

        response = self.client.post(endpoint, {'vote': 1}, format='json')
        expected = {
            'created': True,
            'status': 'vote recorded',
            'display': 'upvote',
            'upvotes': 1,                   # Required for Question FE app (resets button counts)
            'downvotes': 0,                 # Required for Question FE app (resets button counts)
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, val in expected.items():
            self.assertIn(key, response.data)
            self.assertEqual(val, response.data[key])

    @skip("pending implementation")
    def test_question_answers_list(self):
        """
        Ensure GET /api/question/:id/answers response works
        """
        pass

class AnswerAPIViewSetTest(TestCase):

    def setUp(self):
        self.usera  = User.objects.create_user(**fixtures['user'])
        self.userb  = User.objects.create_user(**fixtures['voter'])

        fixtures['question']['author'] = self.usera
        fixtures['answer']['author']   = self.userb

        self.question = Question.objects.create(**fixtures['question'])
        fixtures['answer']['question'] = self.question

        self.client = APIClient()

    def login(self):
        credentials = {
            'username': fixtures['user']['username'],
            'password': fixtures['user']['password'],
        }

        return self.client.login(**credentials)

    def logout(self):
        return self.client.logout();

    def test_answer_url_view_kwarg(self):
        """
        Check that the answer provides a url
        """
        answer   = Answer.objects.create(**fixtures['answer'])
        endpoint = answer.get_api_detail_url()

        self.login()
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url', response.data)

        url      = urlsplit(response.data.get('url', '')).path
        self.assertEqual(url, endpoint)
