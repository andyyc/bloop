from rest_framework import serializers
from api.models import Comment, Game

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_name = serializers.CharField(read_only=True)
    class Meta:
        model = Comment

class GameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=10)
    score = serializers.CharField(max_length=7)

    class Meta:
        model = Game
