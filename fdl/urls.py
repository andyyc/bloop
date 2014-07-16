from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'gm.views.home', name='home'),
    url(r'^accounts/', include('custom_registration.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^draft/', include('draft.urls')),
    # url(r'^fdl/', include('fdl.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
