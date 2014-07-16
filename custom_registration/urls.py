from django.conf.urls import patterns, url
from custom_registration.views import RegistrationView

urlpatterns = patterns('',
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
)