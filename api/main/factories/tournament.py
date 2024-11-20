from utils.faker import faker
from main.models import Tournament
import factory
from .game import GameFactory
from .user import UserFactory

class TournamentFactory(factory.Factory):
    class Meta:
        model = Tournament
    name = factory.Sequence(lambda n: f"tournament{n}")
    description = faker.text()
    game = GameFactory()
    start_date = faker.date()
    end_date = faker.date()
    creator = UserFactory()