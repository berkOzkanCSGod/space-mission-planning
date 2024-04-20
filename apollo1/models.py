from django.db import models, connection
from django.contrib.auth import login

class Users(models.Model):
    uid = models.PositiveIntegerField(primary_key=True, editable=False)
    uname = models.CharField(max_length=100)
    uemail = models.CharField(max_length=100)
    upassword = models.CharField(max_length=100)


    @classmethod
    def getAllUsers(cls):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")

            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = cls(uname=row[1], upassword=row[2])
                users.append(user)
            return users

    @classmethod
    def authenticateUser(cls, uname, upassword):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE uname = %s", [uname])
            row = cursor.fetchone()

            if row:
                if row[3] == upassword:
                    user = cls(uid=row[0], uname=row[1], uemail=row[2], upassword=row[3])
                    return user
                else:
                    return None
            else:
                return None

    @classmethod
    def createUser(cls, uname, uemail, upassword, role):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (uname, uemail, upassword) VALUES ( %s, %s, %s)", [uname, uemail, upassword])
            cursor.execute("SELECT * FROM users WHERE uname = %s", [uname])
            row = cursor.fetchone()
            if row:
                user = cls(uid=row[0], uname=row[1], upassword=row[2])
                cursor.execute("INSERT INTO {} (uid) VALUES (%s)".format(role), [user.uid])
                return user
            else:
                return None
            
    @classmethod
    def getUserByUsername(cls, uname):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE uname = %s", [uname])
            row = cursor.fetchone()

            if row:
                return cls(uname=row[1], upassword=row[2])
            else:
                return None

    @classmethod
    def getUserById(cls, uid, role):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE uid = %s", [uid])
            user_row = cursor.fetchone()
            user_description = cursor.description  # Fetch the description separately

            cursor.execute("SELECT * FROM {} WHERE uid = %s".format(role), [uid])
            role_row = cursor.fetchone()
            role_description = cursor.description  # Fetch the description separately

            if user_row and role_row:
                user_dict = dict(zip([col.name for col in user_description], user_row))
                role_dict = dict(zip([col.name for col in role_description], role_row))

                for key, value in role_dict.items():
                    user_dict[key] = value

                user_dict.update({'role': role})

                return user_dict
            else:
                return None

    @classmethod
    def findUserRole(cls, uid):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM astronaut WHERE uid = %s", [uid])
            row = cursor.fetchone()
            if row:
                return 'astronaut'
            
            cursor.execute("SELECT * FROM organization WHERE uid = %s", [uid])
            row = cursor.fetchone()
            if row:
                return 'organization'
            
    @classmethod
    def updateAttribute(cls, uid, role, attribute, value):
        with connection.cursor() as cursor:
            if (attribute == 'uemail'):
                cursor.execute("UPDATE users SET {} = %s WHERE uid = %s".format(attribute), [value, uid])
                if cursor.rowcount > 0:
                    return None
                else:
                    return "No rows were updated, this email is already taken"
            else:
                cursor.execute("UPDATE {} SET {} = %s WHERE uid = %s".format(role, attribute), [value, uid])
                if cursor.rowcount > 0:
                    return None
                else:
                    return "No rows were updated"
