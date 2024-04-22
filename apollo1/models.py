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

    @classmethod
    def updateAttribute(cls, id, field, input):
        with connection.cursor() as sql:
            sql.execute("UPDATE astronaut SET {} = %s WHERE astro_id = %s".format(field), [input, id])
            res = sql.rowcount > 0
            if res:
                return True

        return False

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

    @classmethod
    def updateAttribute(cls, id, field, input):
        with connection.cursor() as sql:
            sql.execute("UPDATE company SET {} = %s WHERE c_id = %s".format(field), [input, id])
            res = sql.rowcount > 0
            if res:
                return True

        return False