from rest_framework import serializers
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

    class Meta:
        model = Game

class PlaySerializer(serializers.ModelSerializer):
    time = serializers.CharField(max_length=5, min_length=5)

    class Meta:
        model = Play

class CommentBumpSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField(read_only=True)

    class Meta:
        model = CommentBump