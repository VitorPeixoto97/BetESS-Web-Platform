# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Bet(models.Model):
    result = models.IntegerField()
    amount = models.IntegerField()
    odd = models.FloatField()
    profit = models.FloatField()
    event = models.IntegerField()
    user = models.IntegerField()
    def __str__(self):
        return self.result

class Notification(models.Model):
    message = models.CharField(max_length=200)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    user = models.IntegerField()
    def __str__(self):
        return self.bet
