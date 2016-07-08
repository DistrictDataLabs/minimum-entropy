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
from django.views.generic import DetailView, TemplateView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route

##########################################################################
## HTTP Generated Views
##########################################################################

class QuestionDetail(LoginRequired, DetailView):

    model = Question
    template_name = "fugato/question.html"
    context_object_name = "question"

    def get_object(self):
        """
        Ensures the answer order is correct by always calling the set answer
        order method when the object is retrieved from the database.

        TODO: This is expensive! We should only redo the answer order when it
        makes sense (e.g. someone is voting) -- the problem is that the model
        that is being changed (votes for answers) in this case is very far
        from the object that is tracking it (the question). Therefore this is
        the place it makes sense to solve things, but in the future should be
        optimized otherwise this will be a performance drag.
        """
        obj = super(QuestionDetail, self).get_object()
        obj.set_answer_order_by_votes()
        return obj



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
