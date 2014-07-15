from django.conf.urls import patterns,  url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'tweetfindr.views.index', name='index'),
    url(r'^account/(?P<twitter_id>[\d\w\-]+)/?$',
        'tweetfindr.views.find_account', name='find_account'),
)
