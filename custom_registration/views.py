# Create your views here.
from registration.backends.simple.views import RegistrationView as SimpleRegistrationView
from fdl import settings

class RegistrationView(SimpleRegistrationView):
    def get_success_url(self, request, user):
        return settings.LOGIN_REDIRECT_URL