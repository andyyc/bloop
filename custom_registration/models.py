from django.db import models
from registration.signals import user_registered
from gm.models import Manager

def create_manager(sender, user, request, **kwargs):
    Manager.objects.get_or_create(user=user, name=user.username)

user_registered.connect(create_manager)
