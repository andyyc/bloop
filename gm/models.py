from django.db import models
from django.contrib.auth.models import User
from stats.models import Player

# Create your models here.
class Manager(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=64)

class PredraftPick(models.Model):
    manager = models.ForeignKey(Manager)
    player = models.ForeignKey(Player)
    exclude = models.BooleanField()
    class Meta:
        order_with_respect_to = 'manager'