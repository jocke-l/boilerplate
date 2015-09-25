import unittest
import string
from hypothesis import given, assume
from hypothesis.strategies import text
from .python import friendly


def is_ascii(s):
    return all(c in string.printable for c in s)


class FriendlyTestCase(unittest.TestCase):
    @given(text())
    def test_friendly_contains_no_spaces(self, name):
        assume(' ' in name)

        self.assertTrue(all(' ' not in x for x in friendly(name)))

    @given(text())
    def test_friendly_is_ascii(self, name):
        self.assertTrue(all(is_ascii(x) for x in friendly(name)))
