from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'citydigits.views.home', name='home'),

    # create the lottery subdomain
    url(r'^lottery/', include('lottery.urls')),

    # admin docs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # admin
    url(r'^admin/', include(admin.site.urls)),
)
