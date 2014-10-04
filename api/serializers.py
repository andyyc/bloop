from rest_framework import serializers, pagination
from api.models import Comment, Game, Play, CommentBump

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_name = serializers.CharField(read_only=True)
    points_derived = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment

class GameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=10)
    score = serializers.CharField(max_length=7)
    date = serializers.CharField(max_length=6)
    day_of_week = serializers.CharField(max_length=10)
    week = serializers.IntegerField()
    away_team = serializers.CharField(max_length=3)
    home_team = serializers.CharField(max_length=3)
    away_team_icon = serializers.CharField()
    home_team_icon = serializers.CharField()

    class Meta:
        model = Game

class PlaySerializer(serializers.ModelSerializer):
    time = serializers.CharField(max_length=5, min_length=5)
    team_icon = serializers.CharField()

    class Meta:
        model = Play

class PaginatedUserSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = PlaySerializer

class CommentBumpSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField(read_only=True)

    class Meta:
        model = CommentBump