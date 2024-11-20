from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from main.models import Tournament

class UserSerializer(serializers.ModelSerializer):
    tournaments = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    tournaments_created = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'tournaments_created', 'tournaments')

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
