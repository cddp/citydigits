from django.conf.urls import patterns, include, url

from lottery.views import (
            public_splash,
            about,
            interview_photo_grid,
            interview_map,
            public_tutorial,
            user_tutorial,
            interview_split,
            data_explorer,
            api,
        )

urlpatterns = patterns('',

    # public_splash, user home is called by this function
    url(r'^$', public_splash, name="splash"),
    # about
    url(r'^about/$', about, name='about'),

    # interview_photo_grid
    url(r'^interviews/$', interview_photo_grid, name="photo_grid"),
    # interview_map
    url(r'^map/$', interview_map, name="interview_map"),
    # intrview map highlight
    url(r'^map/(\d+)/$', interview_map, name="interview_highlight"),
    # interview_split
    url(r'^map-split/(\d+)/$', interview_split, name="interview_split"),

    url(r'^data/$', data_explorer, name="data_explorer"),

    # model api
    url(r'^api/(\w+)/$', api, name="api"),

    # public_tutorial
    url(r'^tutorial/$', public_tutorial, name="public_tutorial"),
    # user_tutorial
    url(r'^user-tutorial/$', user_tutorial, name="user_tutorial"),

)
