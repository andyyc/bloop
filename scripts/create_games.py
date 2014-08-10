#!/usr/bin/env python
import sys, os
sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fdl.settings")

from api.models import Game, Post
import nfldb

db = nfldb.connect()
q = nfldb.Query(db)

season_year=2014
q.game(season_year=season_year)

for game in q.sort('start_time').as_games():
    name = "%s at %s" % (game.away_team, game.home_team)
    title = "Game thread for %s" % name

    try:
        Game.objects.get(gamekey=game.gamekey)
    except:
        post, post_created = Post.objects.get_or_create(title=title,
                                          points=0)
        game_meta = Game.objects.create(gamekey=game.gamekey,
                                        post=post)
