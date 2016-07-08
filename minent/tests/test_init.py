# minent.tests.test_init
# Initialization tests for the Minimum Entropy project
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jul 05 14:07:25 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: test_init.py [737e142] benjamin@bengfort.com $

"""
Initialization tests for the Minimum Entropy project
"""

##########################################################################
## Imports
##########################################################################

from unittest import TestCase

##########################################################################
## Module variables
##########################################################################

EXPECTED_VERSION = "1.1b2"

##########################################################################
## Initialization Tests
##########################################################################

class InitializationTests(TestCase):
    """
    Some basic minent tests
    """

    def test_sanity(self):
        """
        Check that the world is sane and 2+2=4
        """
        self.assertEqual(2+2, 4)

    def test_import(self):
        """
        Ensure the minent module can be imported
        """
        try:
            import minent
        except ImportError:
            self.fail("Could not import the minent module.")

    def test_version(self):
        """
        Assert that test and package versions match
        """
        import minent
        self.assertEqual(EXPECTED_VERSION, minent.__version__)
