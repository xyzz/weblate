# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2013 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Tests for language manipulations.
"""

from django.test import TestCase
from lang.models import Language
from django.core.management import call_command


class LanguagesTest(TestCase):
    TEST_LANGUAGES = (
        ('cs_CZ', 'cs', 'ltr'),
        ('de-DE', 'de', 'ltr'),
        ('de_AT', 'de_AT', 'ltr'),
        ('ar', 'ar', 'rtl'),
        ('ar_AA', 'ar', 'rtl'),
        ('ar_XX', 'ar_XX', 'rtl'),
    )

    def test_auto_create(self):
        '''
        Tests that auto create correctly handles languages
        '''
        for original, expected, direction in self.TEST_LANGUAGES:
            # Create language
            lang = Language.objects.auto_get_or_create(original)
            # Check language code
            self.assertEqual(lang.code, expected)
            # Check direction
            self.assertEqual(lang.direction, direction)
            # Check whether html contains both language code and direction
            self.assertIn(direction, lang.get_html())
            self.assertIn(expected, lang.get_html())

    def test_plurals(self):
        '''
        Test whether plural form is correctly calculated.
        '''
        lang = Language.objects.get(code='cs')
        self.assertEqual(
            lang.get_plural_form(),
            'nplurals=3; plural=(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2;'
        )


class CommandTest(TestCase):
    '''
    Tests for management commands.
    '''
    def test_setuplang(self):
        call_command('setuplang')
        self.assertTrue(Language.objects.exists())
