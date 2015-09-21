from django.db.models import Manager

__all__ = [
    'SnippetManager'
]


class SnippetManager(Manager):
    def create_with_holder(self, *args, **kwargs):
        from .models import SnippetHolder

        holder = SnippetHolder.objects.create()
        snippet = super().create(*args, holder=holder, **kwargs)

        return snippet, holder
