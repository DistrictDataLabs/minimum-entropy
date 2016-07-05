# users.mixins
# Authentication Mixins
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 15:40:50 2014 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: mixins.py [] benjamin@bengfort.com $

"""
Authentication Mixins
"""

##########################################################################
## Imports
##########################################################################

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

##########################################################################
## Helper functions
##########################################################################

PROFILE_URL = reverse_lazy('profile')

def is_member(user):
    """
    Determines if the logged in user is an authorized member since anyone
    can "register" via the Google OAuth API - once registered, we need
    some other way to give them access or not; namely by having them be a
    part of the Member group.
    """
    if user:
        return user.groups.filter(name='Member').count() > 0
    return False

# The Members only decorator only allows users in that pass is_member
members_only = user_passes_test(is_member, login_url=PROFILE_URL)

##########################################################################
## Mixins
##########################################################################

class MembershipRequired(object):
    """
    Ensures that user must be authenticated in order to access view. They
    must additionally also be part of the Member group - e.g. a complete
    authentication and accepted registration.
    """

    @method_decorator(login_required)
    @method_decorator(members_only)
    def dispatch(self, *args, **kwargs):
        return super(MembershipRequired, self).dispatch(*args, **kwargs)


class LoginRequired(object):
    """
    Ensures that user must be authenticated in order to access view.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs)
