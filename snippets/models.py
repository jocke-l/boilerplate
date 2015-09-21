from django.db import models
from django.contrib.auth.models import User
from .managers import SnippetManager


class SnippetHolder(models.Model):
    @property
    def snippets(self):
        return self.snippet_set.order_by('submitted')

    @property
    def creator(self):
        return self.snippets.first().contributor

    @property
    def contributors(self):
        return User.objects.filter(snippet__holder_id=self.id).distinct()

    @property
    def created(self):
        return self.snippets.first().submitted

    @property
    def latest(self):
        return self.snippets.last()

    def __str__(self):
        return self.snippets.first().name


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
