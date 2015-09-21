from django.test import TestCase
from django.contrib.auth.models import User
from .models import Snippet


class SnippetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.org', 'pass')
        self.user2 = User.objects.create_user('test2', 'test2@example.org',
                                              'pass')

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
            contributor=self.user2,
            name='test',
            description='test description',
            code="print('Changed!')",
        )
        self.assertEquals(holder.snippets[1], change)

        self.assertEquals(holder.creator, self.user)

        self.assertEquals(list(holder.contributors), [self.user, self.user2])

        self.assertEquals(holder.created, snippet.submitted)

        self.assertEqual(holder.latest, change)

        self.assertEqual(str(holder), 'test')
