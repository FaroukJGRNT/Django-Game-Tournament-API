import factory
from django.contrib.auth.models import User
from utils.faker import faker

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n+1}")
    email = factory.Sequence(lambda n: f"user{n+1}@gmail.com")
    password = "defaultpassword"