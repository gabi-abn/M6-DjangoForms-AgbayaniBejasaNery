from django.db import models

# Create your models here.

class Dish(models.Model):
    name = models.CharField(max_length=300)
    prep_time = models.PositiveIntegerField()
    cook_time = models.PositiveIntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.pk) + ": " + self.name

class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) 

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def __str__(self):
        return self.username
    
