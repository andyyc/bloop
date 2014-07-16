from django.db import models
from django.contrib.auth.models import User
from stats.models import Player, Game, PlayerGameStats
from gm.models import Manager

class LeagueTeam(models.Model):
    name = models.CharField(max_length=64)
    league = models.ForeignKey('League')
    manager = models.ForeignKey(Manager)
    commissioner = models.BooleanField(default=False)
    #wins = models.PositiveSmallIntegerField()
    #losses = models.PositiveSmallIntegerField()
    #ties = models.PositiveSmallIntegerField()

class League(models.Model):
    LEAGUE_TYPES = (
        ('S', 'season'),
        ('W', 'single week'),
    )

    LEAGUE_STATUS_CHOICES = (
        ('A', 'active'),
        ('C', 'complete'),
    )
    name = models.CharField(max_length=64)
    lid = models.PositiveIntegerField(unique=True)
    #password = models.CharField(max_length=32)
    league_settings = models.OneToOneField('LeagueSettings', null=True)
    draft_settings = models.OneToOneField('DraftSettings', null=True)
    roster_settings = models.OneToOneField('RosterSettings', null=True)
    scoring_settings = models.OneToOneField('ScoringSettings', null=True)
    current_week = models.ForeignKey('LeagueWeek', null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(Manager, related_name="+")
    type = models.CharField(max_length=1, choices=LEAGUE_TYPES)
    status = models.CharField(max_length=1, choices=LEAGUE_STATUS_CHOICES)
    winner = models.OneToOneField(LeagueTeam, null=True, related_name="+")
    start_week_num = models.PositiveSmallIntegerField(default=1)
    end_week_num = models.PositiveSmallIntegerField(default=18)

class LeagueSettings(models.Model):
    max_teams = models.PositiveSmallIntegerField()

class DraftSettings(models.Model):
    datetime = models.DateTimeField()
    #draft_type = models.CharField()

class RosterSettings(models.Model):
    num_Q = models.PositiveSmallIntegerField(default=1)
    num_R = models.PositiveSmallIntegerField(default=2)
    num_W = models.PositiveSmallIntegerField(default=3)
    num_T = models.PositiveSmallIntegerField(default=1)
    num_W_T = models.PositiveSmallIntegerField(default=0)
    num_W_R = models.PositiveSmallIntegerField(default=0)
    num_W_R_T = models.PositiveSmallIntegerField(default=0)
    num_K = models.PositiveSmallIntegerField(default=1)
    num_D = models.PositiveSmallIntegerField(default=0)

class ScoringSettings(models.Model):
    pass_cmp = models.FloatField(default=0)
    pass_att = models.FloatField(default=0)
    pass_yds = models.FloatField(default=0.04)
    pass_td = models.FloatField(default=4)
    pass_int = models.FloatField(default=-1)
    rec_rec = models.FloatField(default=0.5)
    rec_yds = models.FloatField(default=0.1)
    rec_td = models.FloatField(default=6)
    rush_att = models.FloatField(default=0)
    rush_yds = models.FloatField(default=0.1)
    rush_td = models.FloatField(default=6)    
    two_pt = models.FloatField(default=2)
    fl = models.FloatField(default=-2)

class LeagueRoster(models.Model):
    league_team = models.ForeignKey(LeagueTeam)
    players = models.ManyToManyField(Player, through="RosterPlayer")
    league_week = models.ForeignKey('LeagueWeek', null=True)
    
    def get_fan_pts(self):
        rplayers = self.rosterplayer_set.all()
        total = 0
        for rplayer in rplayers:
            total += rplayer.get_fan_pts()
        return total

class RosterPlayer(models.Model):
    Q = 'Q'
    R = 'R'
    W = 'W'
    T = 'T'
    K = 'K'
    D = 'D'
    WT = 'WT'
    WR = 'WR'
    WRT = 'WRT'

    ROSTER_POSITION_CHOICES = (
        (Q, 'QB'),
        (R, 'RB'),
        (W, 'WR'),
        (T, 'TE'),
        (K, 'K'),
        (D, 'D'),
        (WT, 'W_T'),
        (WR, 'W_R'),
        (WRT, 'W_R_T'),
        )
    roster = models.ForeignKey(LeagueRoster)
    player = models.ForeignKey(Player)
    position = models.CharField(max_length=3, choices=ROSTER_POSITION_CHOICES)

    def get_fan_pts(self, ss):
        games = Game.objects.all()
        try:
            pgs = PlayerGameStats.objects.get(player=self.player,
                                              game__in=games)
        except PlayerGameStats.DoesNotExist:
            return 0

        return (pgs.pass_cmp * ss.pass_cmp +
                pgs.pass_att * ss.pass_att +
                pgs.pass_yds * ss.pass_yds +
                pgs.pass_td * ss.pass_td +
                pgs.pass_int * ss.pass_int +
                pgs.rec_rec * ss.rec_rec +
                pgs.rec_yds * ss.rec_yds +
                pgs.rec_td * ss.rec_td +
                pgs.rush_att * ss.rush_att + 
                pgs.rush_yds * ss.rush_yds + 
                pgs.two_pt * ss.two_pt +
                pgs.fl * ss.fl
                )



"""
class Position(models.Model):
    player = models.ForeignKey(Player)
    lineup = models.ForeignKey(Lineup)
    position = models.CharField(max_length=1, choices=Player.POSITION_CHOICES)
"""
"""
class Match(models.Model):
    league = models.ForeignKey(League)
    league_round = models.ForeignKey(Round)
    home_team = models.ForeignKey(GeneralManager)
    away_team = models.ForeignKey(GeneralManager)
"""
 
class LeagueWeek(models.Model):
    PREDRAFT = '0'
    DRAFTING = '1'
    DRAFTED = '2'
    END = '3'

    LEAGUE_WEEK_STATUS_CHOICES = (
        (PREDRAFT, 'PREDRAFT'),
        (DRAFTING, 'DRAFTING'),
        (DRAFTED, 'DRAFTED'),
        (END, 'END'),
        )
    
    league = models.ForeignKey(League)
    week_num = models.PositiveSmallIntegerField()
    winner = models.ForeignKey(LeagueTeam, null=True)
    status = models.CharField(max_length=1, choices=LEAGUE_WEEK_STATUS_CHOICES)


