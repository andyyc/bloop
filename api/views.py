# Create your views here.
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import json, time
import nfldb
from models import Play, Comment
from rest_framework import permissions

GAME_DAY_FULLNAME_ARRAY = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def week_choices(request):
    time.sleep(1)

    response_data = {
        "week_choices" : [
            "Preseason 0",
            "Preseason 1",
            "Preseason 2",
            "Preseason 3",
            "Preseason 4",
            "Week 1",
            "Week 2",
            "Week 3",
            "Week 4",
            "Week 5",
            "Week 6",
            "Week 7",
            "Week 8",
            "Week 9",
            "Week 10",
            "Week 11",
            "Week 12",
            "Week 13",
            "Week 14",
            "Week 15",
            "Week 16",
            "Week 17"
        ],
        "week_choice_ids" : [
            "PR_0",
            "PR_1",
            "PR_2",
            "PR_3",
            "PR_4",
            "R_1",
            "R_2",
            "R_3",
            "R_4",
            "R_5",
            "R_6",
            "R_7",
            "R_8",
            "R_9",
            "R_10",
            "R_11",
            "R_12",
            "R_13",
            "R_14",
            "R_15",
            "R_16",
            "R_17",
        ]
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


'''
    response_data = {
        "season_year": season_year,
        "season_type": season_type,
        "week": week,
        "scoreboard": [
            {
                "date": "Aug 28",
                "day_of_week": "Thursday",
                "games": [
                    {
                        "gamekey": 54924,
                        "name": "SEA at SFO",
                        "score": "17-20",
                        "time": "4Q/11:58"
                    },
                    {
                        "name": "DEN at NWE",
                        "score": "56-49",
                        "time": "3Q/10:22"
                    },
                    {
                        "name": "PHI at DAL",
                        "score": "20-10",
                        "time": "2Q/5:00"
                    },
                ]
            },
            {
                "date": "2014-08-31",
                "day_of_week": "Sunday",
                "games": [
                    {
                        "name": "SEA at SFO",
                        "score": "17-20",
                        "time": "4Q/11:58"
                    },
                    {
                        "name": "DEN at NWE",
                        "score": "56-49",
                        "time": "3Q/10:22"
                    },
                ]
            },
        ]
    }
'''

def week(request, week_id):
    time.sleep(1)
    print week_id
    week_id_split = week_id.split('_')
    db = nfldb.connect()
    q = nfldb.Query(db)
    season_type = "Regular"

    if week_id_split[0] == "PR":
        season_type = "Preseason"
    elif week_id_split[0] == "R":
        season_type = "Regular"
    elif week_id_split[1] == "P":
        season_type = "Playoff"

    week = week_id_split[1]
    season_year = 2014

    q.game(season_year=season_year,season_type=season_type,week=week)
    scoreboard = []
    dateToGames = {}

    for game in q.sort(('start_time', 'asc')).as_games():
        dow = str(game.day_of_week)
        date = game.start_time.date().strftime("%b %d")
        if date not in dateToGames:
            games = []
            dateToGames = {
                date: games,
            }
            scoreboard_section = {
                "date": date,
                "day_of_week": dow,
                "games": games,
            }
            scoreboard.append(scoreboard_section)
        game_json = {
            "gamekey": game.gamekey,
            "name": "%s at %s" % (game.away_team, game.home_team),
            "score": "%s-%s" % (game.away_score, game.home_score),
        }
        dateToGames[date].append(game_json)

    response_data = {
        "season_year": season_year,
        "season_type": season_type,
        "week": week,
        "scoreboard": scoreboard,
    }
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")


'''
    response_data = {
        "summary": [
            {
                "quarter": "4th Quarter",
                "plays": [
                    {
                        "time": "12:00", "text":"Kaep with the run."
                    },
                    {
                        "time": "13:30", "text":"Gore with the run.",
                        "video": "http://zippy.gfycat.com/UnsungCelebratedAlaskajingle.mp4"
                    },
                ]
            },
            {
                "quarter": "3rd Quarter",
                "plays": [
                    {"time": "2:00", "text":"Russell with the TD."},
                    {"time": "5:30", "text":"Lynch with the run."},
                ]
            }
       ],
        "name": "%s at %s" % (game.away_team, game.home_team),
        "score": "%s-%s" % (game.away_score, game.home_score),
    }
'''

def game(request, gamekey):
    time.sleep(2)
    print gamekey
    db = nfldb.connect()
    q = nfldb.Query(db)

    q.game(gamekey=gamekey)
    game = q.as_games()[0]

    if not game:
        return

    summary = []
    quarterNumToQuarterStringMap = {
        "1": "1st Quarter",
        "2": "2nd Quarter",
        "3": "3rd Quarter",
        "4": "4th Quarter",
    }
    quarterToPlays = {}
    for play in Play.objects.filter(gamekey=gamekey).order_by('quarter', '-time'):
        if play.quarter not in quarterToPlays:
            quarterToPlays[play.quarter] = []
            summary.append(
                {
                    "quarter": quarterNumToQuarterStringMap[play.quarter],
                    "plays": quarterToPlays[play.quarter]
                }
            )
        play_json = {
            "time": play.time,
            "down": play.down,
            "text": play.text,
            "video": play.video_url
        }
        quarterToPlays[play.quarter].append(play_json)

    print summary

    response_data = {
        "summary": summary,
        "name": "%s at %s" % (game.away_team, game.home_team),
        "score": "%s-%s" % (game.away_score, game.home_score),
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


from api.serializers import CommentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from models import Post, Game

class CommentList(generics.ListCreateAPIView):
    queryset = None
    serializer_class = CommentSerializer
    authentication_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        gamekey = request.QUERY_PARAMS.get('gamekey')
        print gamekey
        try:
            game = Game.objects.get(gamekey=gamekey)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(post=game.post)
        serializer = CommentSerializer(comments)
        return Response(serializer.data)
