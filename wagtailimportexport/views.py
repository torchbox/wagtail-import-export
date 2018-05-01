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
    try:
        if export_unpublished:
            root_page = Page.objects.get(id=page_id)
        else:
            root_page = Page.objects.get(id=page_id, live=True)
    except Page.DoesNotExist:
        return JsonResponse({'error': 'page not found'})

    pages = Page.objects.descendant_of(root_page, inclusive=True).order_by('path')
    if not export_unpublished:
        pages = pages.filter(live=True)

    page_data = []
    exported_paths = set()
    for (i, page) in enumerate(pages):
        parent_path = page.path[:-(Page.steplen)]
        # skip over pages whose parents haven't already been exported
        # (which means that export_unpublished is false and the parent was unpublished)
        if i == 0 or (parent_path in exported_paths):
            page_data.append({
                'content': json.loads(page.to_json()),
                'model': page.content_type.model,
                'app_label': page.content_type.app_label,
            })
            exported_paths.add(page.path)

    payload = {
        'pages': page_data
    }

    return JsonResponse(payload)
