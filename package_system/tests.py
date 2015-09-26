import builtins
import string
import unittest
from unittest import mock
from hypothesis import given, assume, example
from hypothesis.strategies import text
from jinja2 import Environment, Template
from .python import friendly, make_package_dir, create_package


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

    @given(text(alphabet=string.printable))  # TODO: Include some unicode
    @example('arst-star')
    def test_friendly_python_not_contains_dashes(self, name):
        _, python_friendly = friendly(name)
        assume(python_friendly != '')

        self.assertNotIn('-', python_friendly)

    def test_friendly_python_dashes_to_underscores(self):
        _, python_friendly = friendly('arst-star')
        self.assertEqual(python_friendly, 'arst_star')


@mock.patch('os.makedirs')
class CreatePackageTestCase(unittest.TestCase):
    def test_package_directory_creation(self, mock_makedirs):
        make_package_dir('.', 1, 'arst star')
        mock_makedirs.assert_called_once_with('./arst-star-1/arst_star')

    def test_package_directory_creation_fail(self, mock_makedirs):
        mock_makedirs.side_effect = OSError
        make_package_dir('.', 1, 'arst star')

    @mock.patch.object(builtins, 'open')
    @mock.patch.object(Environment, 'get_template')
    def test_package_creation(self, mock_get_template, mock_open,
                              mock_makedirs):
        mock_get_template.return_value = Template('{{ name }} {{ version }}')

        mock_write = mock.Mock()
        mock_open.return_value = mock.mock_open().return_value
        mock_open.return_value.write = mock_write

        package_root = create_package('.', {'name': 'arst star', 'version': 1},
                                      'arst = 0')

        self.assertEqual(package_root, './arst-star-1')

        mock_open.assert_any_call('./arst-star-1/setup.py', 'w')
        mock_open.assert_any_call('./arst-star-1/arst_star/__init__.py', 'w')

        mock_write.assert_any_call('arst = 0')
        mock_write.assert_any_call('arst star 1')
