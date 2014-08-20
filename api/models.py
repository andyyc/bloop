from django.db import models
from django.contrib.auth.models import User

class Play(models.Model):
    gamekey = models.CharField(max_length = 5, db_index=True)
    down = models.CharField(max_length = 10)
    text = models.CharField(max_length = 160)
    video_url = models.URLField(blank=True)
    quarter = models.CharField(max_length = 1)
    time = models.CharField(max_length = 5)
    points = models.PositiveIntegerField(default=0)

class CommentBump(models.Model):
    comment = models.ForeignKey('Comment')
    user = models.ForeignKey(User)
    is_removed = models.BooleanField(default=False)

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey('Post')
    parent = models.ForeignKey('self', null=True, blank=True)
    author = models.ForeignKey(User)
    author_name = models.CharField(max_length = 30)
    points = models.PositiveIntegerField(default=0)
    is_removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def points_derived(self):
        return self.commentbump_set.filter(is_removed=False).count()

    def __unicode__(self):
        return u'(%s) %s - %s' % (self.post, self.author, self.text)


class Post(models.Model):
    title = models.CharField(max_length = 128)
    text = models.TextField()
    points = models.PositiveIntegerField(default=0)
    is_removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return u'%s' % self.title

import nfldb
from django.db.models.signals import post_init

class Game(models.Model):
    gamekey = models.CharField(max_length = 5, unique=True)
    post = models.ForeignKey('Post')

    @property
    def name(self):
        return "%s at %s" % (self.nfldb_game.away_team, self.nfldb_game.home_team)

    @property
    def score(self):
        return "%s-%s" % (self.nfldb_game.away_score, self.nfldb_game.home_score)

    @property
    def date(self):
        return self.nfldb_game.start_time.date()

    @property
    def day_of_week(self):
        return str(self.nfldb_game.day_of_week)

    @property
    def season_year(self):
        return self.nfldb_game.season_year

    @property
    def season_type(self):
        return str(self.nfldb_game.season_type)

    @property
    def week(self):
        return self.nfldb_game.week

def handle_game_post_init(**kwargs):
    instance = kwargs.get('instance')
    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game(gamekey=instance.gamekey)
    instance.nfldb_game = q.as_games()[0]

post_init.connect(handle_game_post_init, Game)
