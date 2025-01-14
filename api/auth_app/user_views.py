from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from auth_app.serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# Create your views here.
