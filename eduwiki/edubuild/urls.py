from django.conf.urls import patterns, url
from edubuild import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^build/$', views.build, name='build'),
)
