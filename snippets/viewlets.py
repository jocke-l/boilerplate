from django.template.loader import render_to_string
from viewlet import viewlet
from .models import SnippetHolder


@viewlet
def snippet_rev(context, snippet):
    return render_to_string('viewlets/snippet_rev.html', {'snippet': snippet})


@viewlet
def snippet_list(context):
    holders = SnippetHolder.objects.all()

    return render_to_string('viewlets/snippet_list.html', {'holders': holders})
