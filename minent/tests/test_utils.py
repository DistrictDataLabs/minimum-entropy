# minent.tests.test_utils
# Tests for the utility module of minimum-entropy
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Jun 23 11:53:06 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: test_utils.py [24fa113] benjamin@bengfort.com $

"""
Tests for the utility module of minimum-entropy
"""

##########################################################################
## Imports
##########################################################################

from minent.utils import *
from unittest import TestCase

##########################################################################
## Utilities Testing
##########################################################################

class UtilsTests(TestCase):
    """
    Test the minimum-entropy utilities library
    """

    def test_normalize(self):
        """
        Test the normalization function
        """

        self.assertNotIn(" ", normalize("a b c d e f     g"), "should not contain spaces")
        self.assertNotIn("A", normalize("AAAAA AAA AA 9AA8"), "should not contain uppercase")
        self.assertNotIn(".", normalize("no.punctuation."), "should not contain punctuation")
        self.assertNotIn("-", normalize("no-punctuation-"), "should not contain punctuation")

    def test_normalize_question(self):
        """
        Test question normalization
        """

        testa = "Who is faster, a T-Rex or a Velociraptor?"
        testb = "who is faster? A t-rex or a velociraptor?"

        self.assertEqual(normalize(testa), normalize(testb))

    def test_signature(self):
        """
        Test the text signature method
        """

        self.assertEqual(len(signature("here I am")), 28, "should be base64 encoded SHA1 hash length")
        self.assertEqual(signature("the rain in spain"), b"QKv9wgxE3wSgRQevr3h1S0cg468=", "should compute the correct SHA1 hash")

    def test_question_signature(self):
        """
        Test questions with same signature
        """

        testa = "Who is faster, a T-Rex or a Velociraptor?"
        testb = "who is faster? A t-rex or a velociraptor?"

        self.assertEqual(signature(testa), signature(testb))

    def test_htmlize(self):
        """
        Test the htmlize function
        """

        self.assertEqual(htmlize("http://www.google.com/"), '<p><a href="http://www.google.com/" rel="nofollow">http://www.google.com/</a></p>', "linkify didn't work")
        self.assertNotIn("<script>", htmlize("<script>alert('bad');</script>"), "clean didn't work")
        self.assertIn("<ul>", htmlize("- item 1\n- item 2\n"), "markdown didn't work")
