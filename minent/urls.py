# minent.urls
# The main URL router for the Minimum Entropy application
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 13:30:10 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
The main URL router for the Minimum Entropy application

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

##########################################################################
## Imports
##########################################################################

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from django.views.generic import TemplateView

from users.views import *
from minent.views import *
from fugato.views import *

##########################################################################
## Endpoint Discovery
##########################################################################

## API
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'status', HeartbeatViewSet, "status")
router.register(r'typeahead', QuestionTypeaheadViewSet, "typeahead")

##########################################################################
## Minimum Entropy URL Patterns
##########################################################################

urlpatterns = [
    ## Admin site
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),

    ## Static pages
    url(r'^$', SplashPage.as_view(), name='home'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),

    ## Application Pages
    url(r'^app/$', WebAppView.as_view(), name='app-root'),
    url(r'^q/(?P<slug>[\w-]+)/$', QuestionDetail.as_view(), name='question'),

    ## Authentication
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls')),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),

    ## REST API Urls
    url(r'^api/', include(router.urls, namespace="api")),
]
