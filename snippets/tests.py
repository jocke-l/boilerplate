from django.test import TestCase
from django.contrib.auth.models import User
from .models import Snippet


class SnippetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.org', 'pass')

    def test_snippet(self):
        snippet, holder = Snippet.objects.create_with_holder(
            contributor=self.user,
            name='test',
            description='test description',
            code="print('Hello, world!')"
        )
        self.assertEquals(holder.snippets[0], snippet)

        change = Snippet.objects.create(
            holder=holder,
            contributor=self.user,
            name='test',
            description='test description',
            code="print('Changed!')",
        )
        self.assertEquals(holder.snippets[1], change)
