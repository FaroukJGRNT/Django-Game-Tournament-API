from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=300, null=True)

    def __str__(self) -> str:
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, null=True)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name="tournaments", null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournaments_created')
    participants = models.ManyToManyField(User, related_name='tournaments', default=[])

    def __str__(self) -> str:
        return self.name
