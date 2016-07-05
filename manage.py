#!/usr/bin/env python
# manage.py
# Django default management commands, with some special sauce.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 13:26:09 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: manage.py [] benjamin@bengfort.com $

"""
Django default management commands, with some special sauce.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import dotenv

##########################################################################
## Main Method
##########################################################################

if __name__ == "__main__":
    ## Manage Django Environment
    dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minent.settings")

    ## Execute Django Utility
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
