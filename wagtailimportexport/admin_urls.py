from django.conf.urls import url

from wagtailimportexport import views


app_name = 'wagtailimportexport_admin'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
