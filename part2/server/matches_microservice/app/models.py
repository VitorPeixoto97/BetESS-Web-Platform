from django.db import models
import datetime

class Competition(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    teams = models.ManyToManyField('Team', related_name="competitions")
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    simbolo = models.TextField()
    def __str__(self):
        return self.name

class Event(models.Model):
    type = models.IntegerField()
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    equipaC = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='equipa_casa')
    equipaF = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='equipa_fora')
    oddV = models.DecimalField(max_digits=10, decimal_places=2)
    oddE = models.DecimalField(max_digits=10, decimal_places=2)
    oddD = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    date = models.DateField()
    time = models.TimeField()
    result = models.TextField()
    def __str__(self):
        return self.type