from django.db import models

class Bet(models.Model):
    result = models.IntegerField()
    amount = models.IntegerField()
    odd = models.FloatField()
    profit = models.FloatField()
    def __str__(self):
        return self.result

class Notification(models.Model):
    message = models.CharField(max_length=200)
    def __str__(self):
        return self.message
