from django.conf.urls import patterns, include, url
from api import views

urlpatterns = patterns('',
    url(r'^week-choices/$', "api.views.week_choices", name='week_choices'),
    # url(r'^week/(?P<week_id>\w+)$', "api.views.week", name='week'),
    url(r'^week/(?P<week_id>\w+)$', views.Week.as_view()),
    url(r'^game/(?P<gamekey>[0-9]+)/$', views.GameDetail.as_view()),
    url(r'^comments/$', views.CommentList.as_view()),
    url(r'^plays/$', views.PlayList.as_view()),
    url(r'^comment-bump/$', views.CommentBumpDetails.as_view()),
)
