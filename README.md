# wagtail-import-export
Page export from one Wagtail instance into another

## Installation

Check out this repo somewhere alongside a Wagtail project. From the root of the repo, run:

    pip install -e .

Now add to your project's `INSTALLED_APPS`:

    INSTALLED_APPS = [
        # ...
        'wagtailimportexport'
        # ...
    ]

You should now see an 'Import' item in the Wagtail admin menu.
