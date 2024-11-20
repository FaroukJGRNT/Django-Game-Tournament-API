import django.db
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import Tournament
from main.serializers import TournamentSerializer
from auth_app.serializers import UserSerializer
from main.factories.user import UserFactory
from main.factories.tournament import TournamentFactory

class TournamentAPICase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()

    def test_create_tournament(self):
        self.url = reverse('tournaments_list')
        self.data = {
            'name': 'Test Tournament',
            'description': 'Test tournament for API testing',
            'start_date': '2022-01-01T00:00:00+00:00',
            'end_date': '2022-01-01T00:00:00+00:00'
        }

        # Ensure non-authenticated user is not allowed to create
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticate as user and create tournament
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tournament_created = Tournament.objects.get(name=self.data['name'])
        # Ensure that the data is the same as the reponse data and the db data
        for field_name in self.data.keys():
            db_value = getattr(tournament_created, field_name)
            if field_name == 'start_date' or field_name == 'end_date':
                self.assertEqual(self.data[field_name], db_value.isoformat())
            else:
                self.assertEqual(self.data[field_name], response.data[field_name])
                self.assertEqual(self.data[field_name], db_value)

        # Ensure the owner field is right
        self.assertEqual(response.data['creator'], UserSerializer(self.user).data['username'])

    def test_join_tournament(self):
        self.url = reverse('join_tournament', args=([1]))
        print(self.url)
        tournament = TournamentFactory()
        tournament.game.save()
        tournament.creator.save()
        tournament.save()
        
        # Ensure unauthenticated user cannot join a tournament
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Ensure authenticated user can join a tournament
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the user is in the list of participants
        tournament.refresh_from_db()
        self.assertIn(self.user, tournament.participants.all())

        # Ensure a participant can't join again the same tournament
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_leave_tournament(self):
        self.url = reverse('leave_tournament', args=([1]))
        tournament = TournamentFactory()
        tournament.game.save()
        tournament.creator.save()
        tournament.save()
        tournament.participants.add(self.user)

        # Ensure unauthenticated user cannot leave a tournament
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Ensure authenticated user can leave a tournament
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the user is not in the list of participants
        tournament.refresh_from_db()
        self.assertNotIn(self.user, tournament.participants.all())

        # Ensure a participant can't leave again the same tournament
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_all_tournament(self):
        base_url = reverse('tournaments_list')
        params = '?all=true'
        self.url = f'{base_url}{params}'
        tournament1 = TournamentFactory()
        tournament2 = TournamentFactory()
        tournament1.game.save()
        tournament2.game.save()
        tournament1.creator.save()
        tournament2.creator.save()
        tournament1.save()
        tournament2.save()

        # Ensure unauthenticated user cannot list tournaments
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Ensure authenticated user can list tournaments
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the tournaments are returned in the correct order
        tournaments = Tournament.objects.all()
        self.assertEqual(TournamentSerializer(tournaments, many=True).data, response.data)

    def test_list_tournament(self):
        self.url = reverse('tournaments_list')
        tournament1 = TournamentFactory()
        tournament2 = TournamentFactory()
        tournament1.game.save()
        tournament2.game.save()
        tournament1.creator.save()
        tournament2.creator.save()
        tournament1.save()
        tournament2.save()
        tournament1.participants.add(self.user)
        tournament1.save()

        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the only the first tournament is returned
        tournament = TournamentSerializer(tournament1)
        self.assertEqual(tournament.data['id'], response.data[0]['id'])
        self.assertEqual(len(response.data), 1)
