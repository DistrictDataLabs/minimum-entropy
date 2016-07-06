# users.permissions
# Permissions for Django Rest Framework and other permission classes.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Oct 24 10:20:45 2014 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: permissions.py [] benjamin@bengfort.com $

"""
Permissions for Django Rest Framework and other permission classes.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import permissions

##########################################################################
## Permissions
##########################################################################

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow only owners of an object to edit.
    Note, this permission assumes there is an `author` attribute on the
    object that maps to an `auth.User` instance.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class IsAdminOrSelf(permissions.BasePermission):
    """
    Object-level permission to only allow modifications to a User object
    if the request.user is an administrator or you are modifying your own
    user object.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj
