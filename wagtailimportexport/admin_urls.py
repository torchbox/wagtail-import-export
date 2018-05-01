from django.conf.urls import url

from wagtailimportexport import views


app_name = 'wagtailimportexport'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
