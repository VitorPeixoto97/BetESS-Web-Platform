from django.db import models


class Admin(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.email


class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    clube = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    coins = models.FloatField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Users'