from django.apps import apps

from wagtail.core.models import Page


def import_pages(import_data, parent_page):
    pages_by_original_path = {}
    for (i, page_record) in enumerate(import_data['pages']):
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

    return len(import_data['pages'])
