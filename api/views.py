# Create your views here.
from django.http import HttpResponse, Http404
import json
import nfldb
from models import Play, Comment
from rest_framework import permissions

def week_choices(request):
    response_data = week_choices_dict()
    db = nfldb.connect()
    current_week = nfldb.current(db)
    response_data['current_year'] = current_week[1]
    response_data['current_week'] = current_week[2]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def week_choices_dict():
    return {
        "week_choices" : [
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


from api.serializers import CommentSerializer, GameSerializer, PlaySerializer, CommentBumpSerializer
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from models import Game, CommentBump, Post

class CommentList(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = None
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.author = self.request.user
        obj.author_name = self.request.user.username

    def get(self, request, format=None):
        post_id = request.QUERY_PARAMS.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(post__id=post.id)
        serializer = CommentSerializer(comments, many=True)

        if self.request.user.is_authenticated():
            comment_bumps = CommentBump.objects.filter(comment__id__in=comments, user=self.request.user, is_removed=False)
            comment_bumps_ids = set(comment_bumps.values_list('comment_id', flat=True))

            for comment_data in serializer.data:
                if comment_data['id'] in comment_bumps_ids:
                    comment_data['has_bumped'] = True

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class GameDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, gamekey):
        try:
            return Game.objects.get(gamekey=gamekey)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, gamekey, format=None):
        game = self.get_object(gamekey)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    # def get_nfldb_game(self, gamekey):
    #     db = nfldb.connect()
    #     q = nfldb.Query(db)
    #     q.game(gamekey=gamekey)
    #     nfldb_game = q.as_games()[0]
    #
    #     summary = []
    #     quarterNumToQuarterStringMap = {
    #         "1": "1st Quarter",
    #         "2": "2nd Quarter",
    #         "3": "3rd Quarter",
    #         "4": "4th Quarter",
    #     }
    #     quarterToPlays = {}
    #     for play in Play.objects.filter(gamekey=gamekey).order_by('quarter', '-time'):
    #         if play.quarter not in quarterToPlays:
    #             quarterToPlays[play.quarter] = []
    #             summary.append(
    #                 {
    #                     "quarter": quarterNumToQuarterStringMap[play.quarter],
    #                     "plays": quarterToPlays[play.quarter]
    #                 }
    #             )
    #         play_json = {
    #             "time": play.time,
    #             "down": play.down,
    #             "text": play.text,
    #             "video": play.gfy_url,
    #         }
    #         quarterToPlays[play.quarter].append(play_json)
    #
    #     print summary
    #
    #     response_data = {
    #         "summary": summary,
    #         "name": "%s at %s" % (nfldb_game.away_team, nfldb_game.home_team),
    #         "score": "%s-%s" % (nfldb_game.away_score, nfldb_game.home_score),
    #     }
    #
    #     return response_data

class Week(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, week_id, format=None):
        games = self.games_for_weekid(week_id)
        serializer = GameSerializer(games, many = True)
        return Response(serializer.data)

    @classmethod
    def games_for_weekid(self, week_id):
        db = nfldb.connect()
        q = nfldb.Query(db)
        week_id_split = week_id.split('_')
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
        games = []

        for nfldb_game in q.sort(('start_time', 'asc')).as_games():
            game = Game.objects.get(gamekey=nfldb_game.gamekey)
            games.append(game)

        return games

class PlayList(generics.ListAPIView):
    queryset = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PlaySerializer

    def get(self, request, format=None):
        gamekey = request.QUERY_PARAMS.get('gamekey')
        try:
            Game.objects.get(gamekey=gamekey)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        plays = Play.objects.filter(gamekey=gamekey).order_by('-quarter', 'time')
        serializer = PlaySerializer(plays, many=True)
        return Response(serializer.data)

class PaginatedPlayList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PlaySerializer

    def get_queryset(self):
        queryset = Play.objects.all().order_by('-created_at')
        last_created_at = self.request.QUERY_PARAMS.get('last_created_at', None)
        most_recent_created_at = self.request.QUERY_PARAMS.get('most_recent_created_at', None)
        if last_created_at is not None:
            queryset = queryset.filter(created_at__lt=last_created_at)
        elif most_recent_created_at is not None:
            queryset = queryset.filter(created_at__gt=most_recent_created_at)
        return queryset[:2]


class CommentBumpDetails(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CommentBumpSerializer

    def post(self, request, format=None):
        comment_id = request.DATA.get('comment', None)

        if not comment_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            comment_bump = CommentBump.objects.get(comment__id=comment_id,user=self.request.user)
            serializer = CommentBumpSerializer(comment_bump, data=request.DATA)
            has_bumped_before = True
        except:
            serializer = CommentBumpSerializer(data=request.DATA)
            has_bumped_before = False

        if serializer.is_valid():
            serializer.object.user = self.request.user
            serializer.save()
            if has_bumped_before:
                return Response(serializer.data)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
