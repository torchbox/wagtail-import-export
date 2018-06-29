from django import forms
from django.utils.translation import ugettext as _


WAGTAIL_VERSION_2_OR_GREATER = True


try:
    from wagtail.admin.widgets import AdminPageChooser
    from wagtail.core.models import Page
except ImportError:  # fallback for Wagtail <2.0
    from wagtail.wagtailadmin.widgets import AdminPageChooser
    from wagtail.wagtailcore.models import Page

    WAGTAIL_VERSION_2_OR_GREATER = False


admin_page_params = {
    'can_choose_root': True,
}

if WAGTAIL_VERSION_2_OR_GREATER:
    admin_page_params['user_perms'] = 'copy_to'


class ImportFromAPIForm(forms.Form):
    source_page_id = forms.IntegerField()
    source_site_base_url = forms.URLField()
    parent_page = forms.ModelChoiceField(
        queryset=Page.objects.all(),
        widget=AdminPageChooser(**admin_page_params),
        label=_("Destination parent page"),
        help_text=_("Imported pages will be created as children of this page.")
    )


class ImportFromFileForm(forms.Form):
    file = forms.FileField(label=_("File to import"))
    parent_page = forms.ModelChoiceField(
        queryset=Page.objects.all(),
        widget=AdminPageChooser(**admin_page_params),
        label=_("Destination parent page"),
        help_text=_("Imported pages will be created as children of this page.")
    )


class ExportForm(forms.Form):
    root_page = forms.ModelChoiceField(
        queryset=Page.objects.all(),
        widget=AdminPageChooser(can_choose_root=True),
    )
