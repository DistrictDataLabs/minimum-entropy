# user.admin
# Update the admin interface with the Profile
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Jan 15 16:51:57 2015 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Update the admin interface with the Profile
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from users.models import Profile

##########################################################################
## Inline Adminstration
##########################################################################


class ProfileInline(admin.StackedInline):
    """
    Inline administration descriptor for profile object
    """

    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    """
    Define new User admin
    """

    inlines = (ProfileInline, )

##########################################################################
## Register Admin
##########################################################################

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
