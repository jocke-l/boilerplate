from django.db import models
from django.contrib.auth.models import User
from .managers import SnippetManager


class SnippetHolder(models.Model):
    @property
    def created(self):
        return self.snippets.first().submitted

    @property
    def snippets(self):
        return self.snippet_set.order_by('submitted')

    def __str__(self):
        return str(self.snippets.count())


class Snippet(models.Model):
    holder = models.ForeignKey(SnippetHolder)
    contributor = models.ForeignKey(User)

    submitted = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=255)
    description = models.TextField()
    code = models.TextField()

    objects = SnippetManager()

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)
