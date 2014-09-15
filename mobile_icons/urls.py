from django.conf.urls import patterns, include, url
from mobile_icons import views

urlpatterns = patterns('',
    url(r'^teams/$', "mobile_icons.views.teams", name='teams'),
)
