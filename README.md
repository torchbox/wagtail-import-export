# wagtail-import-export
Page export from one Wagtail instance into another.

A published page and its published descendants can be exported via API or file from a source site and imported into a destination site under an existing page.

The destination site should have the same page models as the source site, with compatible migrations.

## Installation

Check out this repo somewhere alongside a Wagtail project. From the root of the repo, run:

    pip install -e .

Now add to your project's `INSTALLED_APPS`:

    INSTALLED_APPS = [
        # ...
        'wagtailimportexport',
        # ...
    ]

Add the following to your project's urls.py (note that the `include(wagtailimportexport_urls)` line must appear above the `include(wagtail_urls)` line that defines Wagtail's default routes):

    from wagtailimportexport import urls as wagtailimportexport_urls

    urlpatterns = [
        # ...
        url(r'', include(wagtailimportexport_urls)),
        url(r'', include(wagtail_urls)),
    ]


You should now see an 'Import / Export' item in the Wagtail admin menu.

## Configuration

By default only published pages are exported. If a descendant page is unpublished it and all its descendants are pruned (even if some of those descendants are themselves published).

It is possible to export all pages under a source page by adding a setting on the source site:

    WAGTAILIMPORTEXPORT_EXPORT_UNPUBLISHED = True

This should *not* be used in a public source site because the API is unauthenticated and would thus expose unpublished content to anyone.
