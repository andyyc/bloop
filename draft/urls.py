from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^rank/$', "gm.views.gm_rank", name='rank'),
)
