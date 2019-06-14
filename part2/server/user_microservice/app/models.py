from django.db import models

class Admin(models.Model):
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.email

class User(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    type = models.IntegerField(default=0)
    coins = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name