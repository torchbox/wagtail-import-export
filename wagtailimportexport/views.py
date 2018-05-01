import json
import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import requests

from wagtail.core.models import Page

from wagtailimportexport.forms import ImportForm


def index(request):
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            # remove trailing slash from base url
            base_url = re.sub(r'\/$', '', form.cleaned_data['source_site_base_url'])
            import_url = (
                base_url + reverse('wagtailimportexport:export', args=[form.cleaned_data['source_page_id']])
            )
            r = requests.get(import_url)
            import_json = r.json()
            return HttpResponse(repr(import_json), content_type='text/plain')
    else:
        form = ImportForm()

    return render(request, 'wagtailimportexport/import.html', {
        'form': form,
    })


def export(request, page_id, export_unpublished=False):

    def page_json(page):
        return {
            'content': json.loads(page.to_json()),
            'model': page.content_type.model,
            'app_label': page.content_type.app_label,
        }

    def add_published_pages(page):
        payload[page.id] = page_json(page)
        for child_page in page.get_children().live():
            add_published_pages(child_page)

    try:
        page = Page.objects.get(id=page_id, live=True).specific
    except Page.DoesNotExist:
        return JsonResponse({'error': 'page not found'})
    payload = {
        'id': page.id
    }

    if export_unpublished:

        payload[page.id] = page_json(page)
        for subpage in page.get_descendants():
            payload[subpage.id] = page_json(subpage.specific)

    else:

        add_published_pages(page)

    payload['count'] = len(payload) - 1

    return JsonResponse(payload)
