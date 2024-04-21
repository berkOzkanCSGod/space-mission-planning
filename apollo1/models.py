from django.db import models, connection
from django.contrib.auth import login



class Astronaut(models.Model):
    astro_id = models.AutoField(primary_key=True)
    astro_email = models.CharField(max_length=255)
    astro_password = models.CharField(max_length=255)
    astro_creation_date = models.DateField()
    astro_name = models.CharField(max_length=50)
    astro_age = models.IntegerField()
    astro_height = models.IntegerField()
    astro_weight = models.DecimalField(max_digits=10, decimal_places=2)
    astro_experience = models.CharField(max_length=50)
    astro_nationality = models.CharField(max_length=100)


    @classmethod
    def createAstro(cls, aemail, apassword):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM Astronaut WHERE astro_email = %s", [aemail])
            res = sql.fetchone()
            sql.execute("SELECT * FROM Company WHERE c_email = %s", [aemail])
            res1 = sql.fetchone()

            if res is None and res1 is None:
                sql.execute("INSERT INTO Astronaut (astro_email, astro_password) VALUES (%s, %s)", [aemail, apassword])
                sql.execute("SELECT * FROM astronaut WHERE astro_email=%s", [aemail])
                res = sql.fetchone()
                astro_user = cls(
                    astro_id=res[0], 
                    astro_email=res[1],
                    astro_password=res[2], 
                    astro_creation_date=res[3],
                    astro_name=res[4],
                    astro_age=res[5],
                    astro_height=res[6],
                    astro_weight=res[7],
                    astro_experience=res[8],
                    astro_nationality=res[9]
                )    
                return astro_user        
            return res


    @classmethod
    def authenticateUser(cls, email, password):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM astronaut WHERE astro_email=%s", [email])
            res = sql.fetchone()

            if res is not None:
                astro_user = cls(
                    astro_id=res[0], 
                    astro_email=res[1],
                    astro_password=res[2], 
                    astro_creation_date=res[3],
                    astro_name=res[4],
                    astro_age=res[5],
                    astro_height=res[6],
                    astro_weight=res[7],
                    astro_experience=res[8],
                    astro_nationality=res[9]
                )    
                if astro_user.astro_password == password:
                    return astro_user
                else:
                    return None     
            else: 
                return None
    @classmethod
    def findRole(cls, email):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM astronaut WHERE astro_email=%s", [email])
            astro = sql.fetchone()
            sql.execute("SELECT * FROM company WHERE c_email=%s", [email])
            comp = sql.fetchone()
            if astro is not None:
                return 'astronaut'
            elif comp is not None:
                return 'company'
            else:
                return None

    @classmethod
    def getUserById(cls, id):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM astronaut WHERE astro_id=%s", [id])
            res = sql.fetchone()

            if res:
                astro_user = cls(
                    astro_id=res[0], 
                    astro_email=res[1],
                    astro_password=res[2], 
                    astro_creation_date=res[3],
                    astro_name=res[4],
                    astro_age=res[5],
                    astro_height=res[6],
                    astro_weight=res[7],
                    astro_experience=res[8],
                    astro_nationality=res[9]
                )
                return astro_user
            else:
                return None



class Company(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_email = models.CharField(max_length=50, unique=True)
    c_password = models.CharField(max_length=50)
    c_creation_date = models.DateField(auto_now_add=True)
    c_name = models.CharField(max_length=50, blank=True, null=True)
    c_emply_cnt = models.IntegerField(default=0)
    c_country_origin = models.CharField(max_length=50)



    @classmethod
    def createComp(cls, cemail, cpassword):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM Astronaut WHERE astro_email = %s", [cemail])
            res = sql.fetchone()
            sql.execute("SELECT * FROM Company WHERE c_email = %s", [cemail])
            res1 = sql.fetchone()

            if res is None and res1 is None:
                sql.execute("INSERT INTO Company (c_email, c_password) VALUES (%s, %s)", [cemail, cpassword])
                sql.execute("SELECT * FROM Company WHERE c_email=%s", [cemail])
                res = sql.fetchone()
                comp_user = cls(
                    c_id=res[0],
                    c_email=res[1],
                    c_password=res[2],
                    c_creation_date=res[3],
                    c_name=res[4],
                    c_emply_cnt=res[5],
                    c_country_origin=res[6]
                )    

                # create bank account for the company
                sql.execute("INSERT INTO Bank_Account DEFAULT VALUES RETURNING bank_id")
                # sql.execute("SELECT LAST_INSERT_ID()")
                bank_id = sql.fetchone()[0]
                sql.execute("INSERT INTO company_bank_relation (bank_id, c_id) VALUES (%s, %s)", [bank_id, comp_user.c_id])

                return comp_user        
            return res


    @classmethod
    def authenticateUser(cls, email, password):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM company WHERE c_email=%s", [email])
            res = sql.fetchone()

            if res is not None:
                comp_user = cls(
                    c_id=res[0],
                    c_email=res[1],
                    c_password=res[2],
                    c_creation_date=res[3],
                    c_name=res[4],
                    c_emply_cnt=res[5],
                    c_country_origin=res[6]
                )   

                if comp_user.c_password == password:
                    return comp_user
                else:
                    return None     
            else: 
                return None

    @classmethod
    def getUserById(cls, id):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM company WHERE c_id=%s", [id])
            res = sql.fetchone()

            print("Fuck:------------", res)

            if res:
                comp_user = cls(
                    c_id=res[0],
                    c_email=res[1],
                    c_password=res[2],
                    c_creation_date=res[3],
                    c_name=res[4],
                    c_emply_cnt=res[5],
                    c_country_origin=res[6]
                )   
                return comp_user
            else:
                return None




# class Users(models.Model):
#     uid = models.PositiveIntegerField(primary_key=True, editable=False)
#     uname = models.CharField(max_length=100)
#     uemail = models.CharField(max_length=100)
#     upassword = models.CharField(max_length=100)


#     @classmethod
#     def getAllUsers(cls):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users")

#             rows = cursor.fetchall()

#             users = []
#             for row in rows:
#                 user = cls(uname=row[1], upassword=row[2])
#                 users.append(user)
#             return users

#     @classmethod
#     def authenticateUser(cls, uname, upassword):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE uname = %s", [uname])
#             row = cursor.fetchone()

#             if row:
#                 if row[3] == upassword:
#                     user = cls(uid=row[0], uname=row[1], uemail=row[2], upassword=row[3])
#                     return user
#                 else:
#                     return None
#             else:
#                 return None

#     @classmethod
#     def createUser(cls, uname, uemail, upassword, role):
#         with connection.cursor() as cursor:
#             cursor.execute("INSERT INTO users (uname, uemail, upassword) VALUES ( %s, %s, %s)", [uname, uemail, upassword])
#             cursor.execute("SELECT * FROM users WHERE uname = %s", [uname])
#             row = cursor.fetchone()
#             if row:
#                 user = cls(uid=row[0], uname=row[1], upassword=row[2])
#                 cursor.execute("INSERT INTO {} (uid) VALUES (%s)".format(role), [user.uid])
#                 return user
#             else:
#                 return None
            
#     @classmethod
#     def getUserByUsername(cls, uname):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE uname = %s", [uname])
#             row = cursor.fetchone()

#             if row:
#                 return cls(uname=row[1], upassword=row[2])
#             else:
#                 return None

#     @classmethod
#     def getUserById(cls, uid, role):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE uid = %s", [uid])
#             user_row = cursor.fetchone()
#             user_description = cursor.description  # Fetch the description separately

#             cursor.execute("SELECT * FROM {} WHERE uid = %s".format(role), [uid])
#             role_row = cursor.fetchone()
#             role_description = cursor.description  # Fetch the description separately

#             if user_row and role_row:
#                 user_dict = dict(zip([col.name for col in user_description], user_row))
#                 role_dict = dict(zip([col.name for col in role_description], role_row))

#                 for key, value in role_dict.items():
#                     user_dict[key] = value

#                 user_dict.update({'role': role})

#                 return user_dict
#             else:
#                 return None

#     @classmethod
#     def findUserRole(cls, uid):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM astronaut WHERE uid = %s", [uid])
#             row = cursor.fetchone()
#             if row:
#                 return 'astronaut'
            
#             cursor.execute("SELECT * FROM organization WHERE uid = %s", [uid])
#             row = cursor.fetchone()
#             if row:
#                 return 'organization'
            
#     @classmethod
#     def updateAttribute(cls, uid, role, attribute, value):
#         with connection.cursor() as cursor:
#             if (attribute == 'uemail'):
#                 cursor.execute("UPDATE users SET {} = %s WHERE uid = %s".format(attribute), [value, uid])
#                 if cursor.rowcount > 0:
#                     return None
#                 else:
#                     return "No rows were updated, this email is already taken"
#             else:
#                 cursor.execute("UPDATE {} SET {} = %s WHERE uid = %s".format(role, attribute), [value, uid])
#                 if cursor.rowcount > 0:
#                     return None
#                 else:
#                     return "No rows were updated"
