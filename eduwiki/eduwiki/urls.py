from django.conf.urls import patterns, include, url
import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eduwiki.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^eduprototype/', include('eduprototype.urls')),
    url(r'^edubuild/', include('edubuild.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
)
