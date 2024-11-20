from utils.faker import faker
from main.models import Game
import factory

class GameFactory(factory.Factory):
    class Meta:
        model = Game
    name = factory.Sequence(lambda n: f"game{n+1}")
    description = faker.text()
