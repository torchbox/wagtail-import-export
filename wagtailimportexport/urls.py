from django.conf.urls import url

from wagtailimportexport import views


urlpatterns = [
    url(r'^export/(?P<page_id>\d+)/$', views.export, name='export'),
]
