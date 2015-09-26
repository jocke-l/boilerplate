from django.shortcuts import render


def _simple_view_factory(*arg_names, template=None):
    if not template:
        raise TypeError('No template given')

    def view(request, *args):
        return render(
            request, template,
            {arg_name: args[pos]
             for pos, arg_name in enumerate(arg_names)}
        )

    return view


index = _simple_view_factory(template='index.html')
