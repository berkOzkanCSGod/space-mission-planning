from django.db import models

class allUsers(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
        managed = False 

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta: 
        db_table = "users"
