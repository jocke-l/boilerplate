from django.test import TestCase
from django.contrib.auth.models import User
from lxml import html
from .models import Snippet
from .viewlets import snippet_list, snippet_rev


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
            name='test2',
            description='test description',
            code="print('Changed!')",
        )
        self.assertEquals(holder.snippets[1], change)

        self.assertEquals(holder.creator, self.user)

        self.assertEquals(list(holder.contributors), [self.user, self.user2])

        self.assertEquals(holder.created, snippet.submitted)

        self.assertEqual(holder.latest, change)

        self.assertEqual(str(snippet), 'test')

        self.assertEqual(str(holder), 'test2')

    def test_snippet_list(self):
        snippet, holder = Snippet.objects.create_with_holder(
            contributor=self.user,
            name='test',
            description='test description',
            code="print('Hello, world!')"
        )

        change = Snippet.objects.create(
            holder=holder,
            contributor=self.user,
            name='test',
            description='test description',
            code="print('Changed!')",
        )

        snippet2, holder2 = Snippet.objects.create_with_holder(
            contributor=self.user,
            name='test2',
            description='test description',
            code="print('Another world!')"
        )

        result = snippet_list()
        tree = html.fromstring(result)

        self.assertEqual(
            tree.xpath('//code/text()'),
            ["print('Changed!')", "print('Another world!')"]
        )
