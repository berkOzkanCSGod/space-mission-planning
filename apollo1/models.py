from django.db import models, connection
from django.contrib.auth import login

class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    @classmethod
    def getAllUsers(cls):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")

            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = cls(username=row[1], password=row[2])
                users.append(user)
            return users

    @classmethod
    def authenticateUser(cls, username, password):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", [username])

            row = cursor.fetchone()
            if row:
                if row[2] == password:
                    user = cls(id=row[0], username=row[1], password=row[2])
                    return user
                else:
                    return None
            else:
                return None

            
    @classmethod
    def getUserByUsername(cls, username):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", [username])
            row = cursor.fetchone()

            if row:
                return cls(username=row[1], password=row[2])
            else:
                return None
            
    class Meta: 
        db_table = "users"
