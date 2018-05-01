from django.http import HttpResponse
from django.shortcuts import render

from wagtailimportexport.forms import ImportForm


def index(request):
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            return HttpResponse('OK')
    else:
        form = ImportForm()

    return render(request, 'wagtailimportexport/import.html', {
        'form': form,
    })
