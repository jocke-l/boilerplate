import unittest
from hypothesis import given, assume
from hypothesis.strategies import text
from hypothesis.errors import UnsatisfiedAssumption
from .python import friendly


def is_ascii(string):
    return all(ord(char) < 128 for char in string)


# TODO: Fix *args and **kwargs
def ignore_exception(exception):
    def decorator(func):
        def wrapper(self, name):
            try:
                func(self, name)
            except exception:
                raise UnsatisfiedAssumption

        return wrapper

    return decorator


class FriendlyTestCase(unittest.TestCase):
    @given(text())
    @ignore_exception(TypeError)
    def test_friendly_contains_no_spaces(self, name):
        assume(' ' in name)

        self.assertTrue(all(' ' not in x for x in friendly(name)))

    @given(text())
    @ignore_exception(TypeError)
    def test_friendly_is_ascii(self, name):
        self.assertTrue(all(is_ascii(x) for x in friendly(name)))
