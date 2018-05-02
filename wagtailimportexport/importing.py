from django.apps import apps

from wagtail.core.models import Page


def import_pages(import_data, parent_page):
    """
    Take a JSON export of part of a source site's page tree
    and create those pages under the parent page
    """
    pages_by_original_path = {}
    for (i, page_record) in enumerate(import_data['pages']):
        # Get the page model of the source page by app_label and model name
        # The content type ID of the source page is not in general the same
        # between the source and destination sites but the page model needs
        # to exist on both.
        model = apps.get_model(page_record['app_label'], page_record['model'])
        # Create a new page using the content of the source page but clear attributes
        # relating to the source page's position in the source tree.
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
            # Child pages are created in the same sibling path order as the
            # source tree because the export is ordered by path
            parent_path = original_path[:-(Page.steplen)]
            pages_by_original_path[parent_path].add_child(instance=page)

        pages_by_original_path[original_path] = page

    return len(import_data['pages'])
