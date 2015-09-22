from django.contrib import admin
from .models import SnippetHolder, Snippet


class SnippetInline(admin.StackedInline):
    model = Snippet


@admin.register(SnippetHolder)
class SnippetHolderAdmin(admin.ModelAdmin):
    inlines = [SnippetInline]
