from django.db import models
import datetime

class Competition(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
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
    oddV = models.FloatField()
    oddE = models.FloatField()
    oddD = models.FloatField()
    status = models.BooleanField(default=True)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(default=datetime.datetime.now().strftime('%H:%M'))
    result = models.TextField()
    def __str__(self):
        return self.type