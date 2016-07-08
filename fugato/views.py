# fugato.views
# Views for the Fugato app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 23 15:05:12 2014 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the Fugato app
"""

##########################################################################
## Imports
##########################################################################

from fugato.models import *
from voting.models import Vote
from tagging.models import Tag
from fugato.serializers import *
from voting.serializers import *
from rest_framework import viewsets
from users.mixins import LoginRequired
from users.permissions import IsAuthorOrReadOnly
from tagging.serializers import CSVTagSerializer
from django.views.generic import DetailView, ListView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route

##########################################################################
## HTTP Generated Views
##########################################################################

class QuestionList(LoginRequired, ListView):
    """
    Authenticated web application view that serves all context and content
    to kick off the Backbone front-end application.
    """

    model = Question
    template_name = "fugato/list.html"
    context_object_name = 'question_list'
    paginate_by = 20

    def get_queryset(self):
        """
        Performs filtering on the queryset based on the query arguments.
        """
        queryset = super(QuestionList, self).get_queryset()

        # Get possible tag and sort options from the query string
        self.sorted_by = self.request.GET.get('sort', 'recent').lower()
        self.tagged_by = self.request.GET.get('tag', None)

        # Select the order by key constraint
        if self.sorted_by == 'recent':
            queryset = queryset.order_by('-modified')

        elif self.sorted_by == 'newest':
            queryset = queryset.order_by('-created')

        elif self.sorted_by == 'popular':
            queryset = queryset.count_votes().order_by('-num_votes')

        elif self.sorted_by == 'frequent':
            queryset = queryset.count_answers().order_by('-num_answers')

        elif self.sorted_by == 'unanswered':
            queryset = queryset.unanswered()

        else:
            # This is the default, but possibly should warn or except
            self.sorted_by = 'recent'
            queryset = queryset.order_by('-modified')

        # Construct the queryset request
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)

        # Add query params for the view
        context['sort'] = self.sorted_by
        context['tag']  = self.tagged_by

        # TODO: This might be very slow, improve this!
        context['num_all_questions'] = self.model.objects.count()

        return context


class QuestionDetail(LoginRequired, DetailView):

    model = Question
    template_name = "fugato/question.html"
    context_object_name = "question"


##########################################################################
## API HTTP/JSON Views
##########################################################################

class QuestionTypeaheadViewSet(viewsets.ViewSet):
    """
    Endpoint for returning a typeahead of question texts.
    """

    def list(self, request):
        queryset = Question.objects.values_list('text', flat=True)
        return Response(queryset)


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.order_by('-created')
    serializer_class   = QuestionSerializer

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """
        Note that the upvotes and downvotes keys are required by the front-end
        """
        question   = self.get_object()
        serializer = VotingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():

            kwargs = {
                'content': question,
                'user': request.user,
                'vote': serializer.validated_data['vote'],
            }

            # Vote for the question
            _, created = Vote.objects.punch_ballot(**kwargs)

            # Construct the Response
            response = serializer.data
            response.update({'status': 'vote recorded', 'created': created,
                             'upvotes': question.votes.upvotes().count(),
                             'downvotes': question.votes.downvotes().count()})
            return Response(response)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def tags(self, request, pk=None):
        """
        A helper endpoint to post tags represented as CSV data.
        """
        question   = self.get_object()

        if request.method == 'GET':
            return Response(CSVTagSerializer.serialize_question(question))

        serializer = CSVTagSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # First add any tags to the question
            for tag in serializer.validated_data['csv_tags']:
                # Don't add tags again (minimize db queries )
                if question.has_tag(tag): continue

                # Otherwise, get or create the tag
                tag, _ = Tag.objects.get_or_create(
                    text = tag,
                    defaults = {
                        'creator': request.user,
                    }
                )

                # Add the tag to the question object
                question.tags.add(tag)

            # Next delete any tags that were removed from the question
            for tag in question.tags.all():
                if tag.text not in serializer.validated_data['csv_tags']:
                    question.tags.remove(tag)

            return Response(CSVTagSerializer.serialize_question(question))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def answers(self, request, pk=None):
        """
        Returns a list of all answers associated with the question
        """
        question   = self.get_object()
        answers    = question.answers.order_by('created') # TODO: order by vote count
        page       = self.paginate_queryset(answers)

        if page is not None:
            serializer = AnswerSerializer(page, context={'request': request})
            paginator  = self.pagination_class()
            return self.get_paginated_response(serializer.data)

        serializer = AnswerSerializer(answers, context={'request': request})
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):

    queryset = Answer.objects.order_by('-created')
    serializer_class = AnswerSerializer

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """
        Note that the upvotes and downvotes keys are required by the front-end
        """
        answer   = self.get_object()
        serializer = VotingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():

            kwargs = {
                'content': answer,
                'user': request.user,
                'vote': serializer.validated_data['vote'],
            }

            _, created = Vote.objects.punch_ballot(**kwargs)
            response = serializer.data
            response.update({'status': 'vote recorded', 'created': created,
                             'upvotes': answer.votes.upvotes().count(),
                             'downvotes': answer.votes.downvotes().count()})
            return Response(response)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
