import json
import re

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ungettext
import requests

from wagtail.admin import messages
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
            pages_by_original_path = {}
            parent_page = form.cleaned_data['parent_page']
            for (i, page_record) in enumerate(import_json['pages']):
                model = apps.get_model(page_record['app_label'], page_record['model'])
                page = model.from_serializable_data(page_record['content'], check_fks=True, strict_fks=False)
                original_path = page.path
                page.id = None
                page.path = None
                page.depth = None
                page.numchild = 0
                page.url_path = None
                if i == 0:
                    parent_page.add_child(instance=page)
                else:
                    parent_path = original_path[:-(Page.steplen)]
                    pages_by_original_path[parent_path].add_child(instance=page)

                pages_by_original_path[original_path] = page

            page_count = len(import_json['pages'])
            messages.success(request, ungettext(
                "%(count)s page imported.",
                "%(count)s pages imported.",
                page_count) % {'count': page_count}
            )
            return redirect('wagtailadmin_explore', parent_page.pk)
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

    pages = Page.objects.descendant_of(root_page, inclusive=True).order_by('path').specific()
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
