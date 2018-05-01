from django.conf.urls import include, url
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.menu import MenuItem
from wagtailimportexport import admin_urls
from wagtail.core import hooks


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^import/', include(admin_urls, namespace='wagtailimportexport_admin')),
    ]


class ImportMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.is_superuser


@hooks.register('register_admin_menu_item')
def register_import_menu_item():
    return ImportMenuItem(
        _('Import'), reverse('wagtailimportexport_admin:index'), classnames='icon icon-download', order=800
    )
