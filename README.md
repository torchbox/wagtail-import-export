# wagtail-import-export
Page export from one Wagtail instance into another

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


You should now see an 'Import' item in the Wagtail admin menu.
