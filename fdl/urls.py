from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from rest_framework import routers

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = patterns('',
    # Examples:
    #url(r'^api/', include(router.urls)),
    # for logging into the browsable api
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('api.urls')),
#    url(r'^$', 'gm.views.home', name='home'),
#    url(r'^draft/', include('draft.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^fdl/', include('fdl.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
