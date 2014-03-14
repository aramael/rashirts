from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'rashirtme.views.home', name='home'),
    url(r'^pay/$', 'rashirtme.views.process_order', name='process_order'),
    url(r'^admin/', include(admin.site.urls)),
)