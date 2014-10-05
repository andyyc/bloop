from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

team_icon_dict = {
        "ARI":static("team_icons/ARI.png"),
        "ATL":static("team_icons/ATL.png"),
        "BAL":static("team_icons/BAL.png"),
        "BUF":static("team_icons/BUF.png"),
        "CAR":static("team_icons/CAR.png"),
        "CHI":static("team_icons/CHI.png"),
        "CIN":static("team_icons/CIN.png"),
        "CLE":static("team_icons/CLE.png"),
        "DAL":static("team_icons/DAL.png"),
        "DEN":static("team_icons/DEN.png"),
        "DET":static("team_icons/DET.png"),
        "GB":static("team_icons/GB.png"),
        "HOU":static("team_icons/HOU.png"),
        "IND":static("team_icons/IND.png"),
        "JAC":static("team_icons/JAC.png"),
        "KC":static("team_icons/KC.png"),
        "MIA":static("team_icons/MIA.png"),
        "MIN":static("team_icons/MIN.png"),
        "NE":static("team_icons/NE.png"),
        "NO":static("team_icons/NO.png"),
        "NYG":static("team_icons/NYG.png"),
        "NYJ":static("team_icons/NYJ.png"),
        "OAK":static("team_icons/OAK.png"),
        "PHI":static("team_icons/PHI.png"),
        "PIT":static("team_icons/PIT.png"),
        "SD":static("team_icons/SD.png"),
        "SEA":static("team_icons/SEA.png"),
        "SF":static("team_icons/SF.png"),
        "STL":static("team_icons/STL.png"),
        "TB":static("team_icons/TB.png"),
        "TEN":static("team_icons/TEN.png"),
        "WAS":static("team_icons/WAS.png"),
    }

class Play(models.Model):
    QUARTER_CHOICES = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', 'OT'),
    )

    gamekey = models.CharField(max_length = 5, db_index=True)
    down = models.CharField(blank=True, max_length = 10)
    text = models.CharField(max_length = 160)
    gfy_id = models.CharField(blank=True, max_length = 128)
    mp4_url = models.CharField(blank=True, max_length = 128)
    quarter = models.CharField(max_length = 1, choices=QUARTER_CHOICES)
    time = models.CharField(max_length = 5)
    points = models.PositiveIntegerField(default=0)
    team = models.CharField(max_length = 3, blank=True)
    score = models.CharField(max_length = 7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('Post', null=True)

    @property
    def team_icon(self):
        if self.team:
            return team_icon_dict[self.team]
        else:
            return ""

    @property
    def gfy_url(self):
        if self.gfy_id:
            return "http://gfycat.com/" + self.gfy_id
        else:
            return ""


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
    def away_team(self):
        return self.nfldb_game.away_team

    @property
    def home_team(self):
        return self.nfldb_game.home_team

    @property
    def away_team_icon(self):
        return team_icon_dict[self.nfldb_game.away_team]

    @property
    def home_team_icon(self):
        return team_icon_dict[self.nfldb_game.home_team]

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
    db.close()

post_init.connect(handle_game_post_init, Game)
