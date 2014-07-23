from django.db import models

class Play(models.Model):
    gamekey = models.CharField(max_length = 5, db_index=True)
    down = models.CharField(max_length = 10)
    text = models.CharField(max_length = 160)
    video_url = models.URLField(blank=True)
    quarter = models.CharField(max_length = 1)
    time = models.CharField(max_length = 5)

