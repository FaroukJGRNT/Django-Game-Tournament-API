from rest_framework import serializers
from .models import Game, Tournament
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'description')

class TournamentSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field='username')
    game = serializers.SlugRelatedField(read_only=True, slug_field='name')
    participants = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')
    class Meta:
        model = Tournament
        fields = ('id', 'name', 'description', 'game', 'start_date', 'end_date', 'creator', 'participants')

