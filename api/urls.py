from django.conf.urls import patterns, include, url
from tastypie.api import Api
#from resources import MyModelResource

# v1_api = Api(api_name='v1')
# v1_api.register(MyModelResource())

# urlpatterns = patterns('',
  # ...more URLconf bits here...
  # Then add:
#  (r'^api/', include(v1_api.urls)),
# )

urlpatterns = patterns('',
    url(r'^week-choices/$', "api.views.week_choices", name='week_choices'),
    url(r'^week/(?P<week_id>\w+)$', "api.views.week", name='week'),
    url(r'^game/(?P<gamekey>[0-9]+)/$', "api.views.game", name='game'),
)
