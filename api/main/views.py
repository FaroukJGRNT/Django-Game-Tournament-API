from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth_app.serializers import UserSerializer
from .serializers import  TournamentSerializer
from .models import Tournament
from django.contrib.auth.models import User
from rest_framework import status

@api_view(['GET'])
def tournament_detail(request, pk):
    tournament = Tournament.objects.get(id=pk)
    serializer = TournamentSerializer(tournament)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def tournament_list(request):
    if request.method == 'GET':
        wants_all = request.query_params.get('all', False)
        if wants_all:
            tournaments = Tournament.objects.all()
        else:
            tournaments = Tournament.objects.filter(participants=request.user)
        serializer = TournamentSerializer(tournaments, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def join_tournament(request, pk):
    # Get the tournament from db
    tournament = Tournament.objects.get(pk=pk)
    if request.user not in tournament.participants.all():

        # Add the requesting user to the participants
        tournament.participants.add(request.user)

        # Get the updated tournament data and return it as response
        deserialized_tournament = TournamentSerializer(tournament)
        return Response(deserialized_tournament.data, status=status.HTTP_200_OK)

    elif request.user in tournament.participants.all():
        return Response({'error': 'User is already a participant'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def leave_tournament(request, pk):
    tournament = Tournament.objects.get(pk=pk)

    if request.user in tournament.participants.all():
        tournament.participants.remove(request.user)

        deserialized_tournament = TournamentSerializer(tournament)
        return Response(deserialized_tournament.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'User is not a participant'}, status=status.HTTP_400_BAD_REQUEST)
