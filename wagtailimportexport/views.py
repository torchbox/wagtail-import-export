import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from wagtail.core.models import Page

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


def export(request, page_id):

    def page_json(page):
        return {
            'content': json.loads(page.to_json()),
            'model': page.content_type.model,
            'app_label': page.content_type.app_label,
        }

    try:
        page = Page.objects.get(id=page_id, live=True).specific
    except Page.DoesNotExist:
        return JsonResponse({'error': 'page not found'})
    payload = {
        'id': page.id
    }
    payload[page.id] = page_json(page)
    for subpage in page.get_descendants():
        payload[subpage.id] = page_json(subpage.specific)

    return JsonResponse(payload)
