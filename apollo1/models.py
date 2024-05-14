from django.db import models, connection
from django.contrib.auth import login
from decimal import Decimal

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_email = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=50)
    admin_creation_date = models.DateField(auto_now_add=True)

    @classmethod
    def authenticateUser(cls, email, password):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM admin WHERE admin_email=%s", [email])
            res = sql.fetchone()

            if res is not None:
                admin_user = cls(
                    admin_id=res[0],
                    admin_email=res[1],
                    admin_password=res[2],
                    admin_creation_date=res[3]
                )

                if admin_user.admin_password == password:
                    return admin_user
                else:
                    return None
            else:
                return None

    @classmethod
    def getUserById(cls, id):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM admin WHERE admin_id=%s", [id])
            res = sql.fetchone()

            if res:
                admin_user = cls(
                    admin_id=res[0],
                    admin_email=res[1],
                    admin_password=res[2],
                    admin_creation_date=res[3]
                )
                return admin_user
            else:
                return None

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
            sql.execute("SELECT * FROM admin WHERE admin_email=%s", [email])
            admin = sql.fetchone()
            if astro is not None:
                return 'astronaut'
            elif comp is not None:
                return 'company'
            elif admin is not None:
                return 'admin'
            else:
                return None

    @classmethod
    def getAstronautTrainings(cls, id):
        with connection.cursor() as sql:
            sql.execute("SELECT T.t_id, T.t_name, T.t_description, C.status FROM training T, completes C WHERE C.astro_id=%s AND C.t_id = T.t_id ORDER BY T.t_id ASC", [id])
            return sql.fetchall()

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
    
    def getPerformingMissions(id):
        with connection.cursor() as sql:
            sql.execute("SELECT SM.sm_id, SM.sm_name, SM.sm_duration, SM.sm_destination, SM.sm_astro_cnt, SM.sm_objective FROM assigned_to AT JOIN space_mission SM ON AT.sm_id = SM.sm_id AND AT.astro_id = %s", [id])
            return sql.fetchall()


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
                sql.execute("INSERT INTO owns (bank_id, c_id) VALUES (%s, %s)", [bank_id, comp_user.c_id])

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
    
    def getCreatedMissions(id):
        with connection.cursor() as sql:
            sql.execute("SELECT SM.sm_id, SM.sm_name, SM.sm_duration, SM.sm_destination, SM.sm_astro_cnt, SM.sm_objective FROM creates_mission CM JOIN Space_Mission SM ON CM.sm_id = SM.sm_id AND CM.c_id = %s", [id])
            return sql.fetchall()

    def getPerformingMissions(id):
        with connection.cursor() as sql:
            sql.execute("SELECT SM.sm_id, SM.sm_name, SM.sm_duration, SM.sm_destination, SM.sm_astro_cnt, SM.sm_objective FROM performing_missions PM JOIN Space_Mission SM ON PM.sm_id = SM.sm_id AND PM.c_id = %s", [id])
            return sql.fetchall()

    def getMostActiveCreatorCompany():
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM company WHERE c_id = (SELECT c_id FROM creates_mission GROUP BY c_id ORDER BY COUNT(sm_id) DESC LIMIT 1)")
            return sql.fetchall()

    def getMostActiveExecutorCompany():
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM company WHERE c_id = (SELECT c_id FROM performing_missions GROUP BY c_id ORDER BY COUNT(sm_id) DESC LIMIT 1)")
            return sql.fetchall()
        
    def getAstronauts(id):
        with connection.cursor() as sql:
            sql.execute("SELECT * from astronaut WHERE astro_id IN (SELECT WF.astro_id FROM works_for WF WHERE WF.c_id = %s)", [id])
            return sql.fetchall()
        
    def getTrainedAstronauts(sm_id, c_id):
        with connection.cursor() as sql:
            requiredTrainings = Space_Mission.getRequiredTrainings(sm_id)
            if len(requiredTrainings) == 0:
                return Company.getAstronauts(c_id)
            else:
                sql.execute("""
                SELECT A.* 
                FROM astronaut A
                JOIN works_for WF ON A.astro_id = WF.astro_id
                JOIN completes C ON A.astro_id = C.astro_id
                JOIN required R ON C.t_id = R.t_id
                WHERE WF.c_id = %s AND R.sm_id = %s AND C.status = 0
                GROUP BY A.astro_id
                HAVING COUNT(DISTINCT R.t_id) = (SELECT COUNT(DISTINCT t_id) FROM required WHERE sm_id = %s)
                """, [c_id, sm_id, sm_id])
                return sql.fetchall()


class Launch_Site(models.Model):
    ls_id = models.AutoField(primary_key=True)
    ls_launch_cost = models.DecimalField(max_digits=10, decimal_places=2)
    ls_location = models.CharField(max_length=50)

    @classmethod 
    def isAvailable(cls, id, time):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM uses WHERE launch_time=%s AND ls_id=%s",[time,id])
            res = sql.fetchone()
            if res is not None:
                return False
            
        return True


class Space_Mission(models.Model):
    sm_id = models.AutoField(primary_key=True)
    sm_name = models.CharField(max_length=50)
    sm_duration = models.DecimalField(max_digits=10, decimal_places=2)
    sm_destination = models.CharField(max_length=50)
    sm_astro_cnt = models.IntegerField(default=1)
    sm_objective = models.TextField()

    
    def createMission(c_id, name, dest, duration, astroCnt, objective, launchSite, launchTime):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM launch_site WHERE ls_location=%s",[launchSite])
            res = sql.fetchone()
            ls = Launch_Site(
                ls_id=res[0],
                ls_location=res[1],
                ls_launch_cost=res[2]
            )

            # check if launch site is available on that time
            if ls.isAvailable(ls.ls_id, launchTime) is False:
                return None

            sql.execute("INSERT INTO space_mission (sm_name, sm_duration, sm_destination, sm_astro_cnt, sm_objective) VALUES (%s, %s, %s, %s, %s)", [name, duration, dest, astroCnt, objective])
            sql.execute("SELECT * FROM space_mission WHERE sm_name=%s",[name])
            res = sql.fetchone()

            mission_id = res[0]

            sql.execute("INSERT INTO uses (ls_id, sm_id, launch_time) VALUES (%s, %s, %s)", [ls.ls_id, mission_id, launchTime])
            sql.execute("INSERT INTO creates_mission (c_id, sm_id) VALUES (%s, %s)", [c_id, mission_id])

            return True

    def getLaunchSites():
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM launch_site")
            return sql.fetchall()
        
    def getAllMissions():
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM allmissions")
            return sql.fetchall()
        
    def filter(filter, order_field, order_direction):
        with connection.cursor() as sql:
            order_query = f" ORDER BY {order_field} {order_direction}" if order_field else ""
            
            if filter == 'bidding':
                sql.execute(f'''SELECT sm_name, sm_duration, sm_destination, sm_astro_cnt, c_name, c_country_origin FROM space_mission SM 
                            JOIN creates_mission CM ON SM.sm_id = CM.sm_id 
                            JOIN company C ON CM.c_id = C.c_id
                            WHERE CM.status = 'Bidding'{order_query}
                            ''')
                return sql.fetchall()
            elif filter == 'in_progress':
                sql.execute(f'''SELECT sm_name, sm_duration, sm_destination, sm_astro_cnt, c_name, c_country_origin FROM space_mission SM 
                            JOIN performing_missions PM ON SM.sm_id = PM.sm_id 
                            JOIN company C ON PM.c_id = C.c_id
                            WHERE PM.status = 'Incomplete'{order_query}
                            ''')
                return sql.fetchall()
            elif filter == 'completed':
                sql.execute(f'''SELECT sm_name, sm_duration, sm_destination, sm_astro_cnt, c_name, c_country_origin FROM space_mission SM 
                            JOIN performing_missions PM ON SM.sm_id = PM.sm_id 
                            JOIN company C ON PM.c_id = C.c_id
                            WHERE PM.status = 'Success' OR PM.status = 'Failure' {order_query}
                            ''')
                return sql.fetchall()
            else:
                sql.execute(f'''SELECT sm_name, sm_duration, sm_destination, sm_astro_cnt, c_name, c_country_origin FROM space_mission SM 
                            JOIN creates_mission CM ON SM.sm_id = CM.sm_id 
                            JOIN company C ON CM.c_id = C.c_id{order_query}
                            ''')
                return sql.fetchall()
            
    def getMissionByName(name):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM space_mission WHERE sm_name=%s", [name])
            return sql.fetchone()
    
    def getMissionById(sm_id):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM space_mission WHERE sm_id=%s", [sm_id])
            return sql.fetchone()

    def findIdByName(name):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM space_mission WHERE sm_name=%s", [name])
            row = sql.fetchone()
            if row:
                return row[0]
            else:
                return None

    def findCreatorId(sm_id):
        with connection.cursor() as sql:
            sql.execute('''
                            SELECT c_id 
                            FROM creates_mission
                            WHERE sm_id=%s       
                        ''', [sm_id])
            return sql.fetchone()[0]

    def findBids(sm_id):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM bids WHERE sm_id=%s", [sm_id])
            return sql.fetchall()

    def findPerformingMission(sm_id):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM performing_missions WHERE sm_id=%s", [sm_id])
            return sql.fetchone()
        
    def placeBid(sm_id, c_id, amount):
        with connection.cursor() as sql:
            # do checks for balance etc., etc.,

            sql.execute("INSERT INTO bids (sm_id, c_id, amount) VALUES (%s, %s, %s)", [sm_id, c_id, amount])
            return None

    def acceptBid(sm_id, c_id):
        with connection.cursor() as sql:
            sql.execute("INSERT INTO performing_missions (c_id, sm_id) VALUES (%s,%s)", [c_id, sm_id])

    def updateStatus(sm_id, status):
        with connection.cursor() as sql:
            sql.execute("UPDATE performing_missions SET status = %s WHERE sm_id = %s", [status, sm_id])

    def getRequiredTrainings(id):
        with connection.cursor() as sql:
            sql.execute("SELECT T.t_id, T.t_name, T.t_description FROM training T, required R WHERE R.sm_id=%s AND R.t_id = T.t_id ORDER BY T.t_id ASC", [id])
            return sql.fetchall()

    def getMostExpensiveMission(): 
        with connection.cursor() as sql:
            sql.execute("SELECT SM.* FROM space_mission SM, (SELECT B.sm_id FROM bids B, performing_missions PM WHERE PM.sm_id = B.sm_id GROUP BY B.sm_id ORDER BY MAX(B.amount) DESC LIMIT 1) AS T WHERE SM.sm_id = T.sm_id")
            return sql.fetchall()

    def getMissionWithMostAstronauts():
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM space_mission WHERE sm_astro_cnt = (SELECT MAX(sm_astro_cnt) FROM space_mission)")
            return sql.fetchall()

    def getMissionWithHighestBid():
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM space_mission WHERE sm_id = (SELECT sm_id FROM bids GROUP BY sm_id ORDER BY MAX(amount) DESC LIMIT 1)")
            return sql.fetchall()
        
    def assignAstro(sm_id, astro_id):
        with connection.cursor() as sql:
            sql.execute("INSERT INTO assigned_to (astro_id, sm_id) VALUES (%s, %s)", [astro_id, sm_id])

    def fireAstro(sm_id, astro_id):
        with connection.cursor() as sql:
            sql.execute("DELETE FROM assigned_to WHERE astro_id=%s AND sm_id=%s", [astro_id, sm_id])

    def getAssignedAstronauts(sm_id):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM astronaut WHERE astro_id IN (SELECT astro_id FROM assigned_to WHERE sm_id=%s)", [sm_id])
            return sql.fetchall()


class Bank_Account(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2)
    bank_company_id = models.ForeignKey(Company, on_delete=models.CASCADE)  # company that owns the bank account
    bank_account_number = models.CharField(max_length=50)

    def createBankAccount(c_id, bank_account_number):
        with connection.cursor() as sql:
            sql.execute("""
            INSERT INTO bank_account (bank_balance, bank_company_id, bank_account_number) VALUES (100000, %s, %s) RETURNING bank_id
            """, [c_id, bank_account_number])
            bank_id = sql.fetchone()[0]
            sql.execute("INSERT INTO owns (bank_id, c_id) VALUES (%s, %s)", [bank_id, c_id])
            return bank_id

    def getBalance(bank_id):
        with connection.cursor() as sql:
            sql.execute("SELECT bank_balance FROM bank_account WHERE bank_id=%s", [bank_id])
            acc = sql.fetchone()
            if acc is None:
                print("No bank account found")
                return None
            balance = acc[0]
            return balance

    def getBankAccountId(c_id):
        with connection.cursor() as sql:
            sql.execute("SELECT bank_id FROM owns WHERE c_id=%s", [c_id])
            res = sql.fetchone()
            if res is None:
                return None
            return res[0]

    def getBankAccount(c_id):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM owns WHERE c_id=%s", [c_id])  # get the bank_id from owns table
            res = sql.fetchone()
            if res is None:
                return None
            sql.execute("SELECT * FROM bank_account WHERE bank_id=%s", [res[0]])
            account = sql.fetchone()
            return account

    def updateBalance(bank_id, amount):
        with connection.cursor() as sql:
            balance = Bank_Account.getBalance(bank_id)
            if not isinstance(amount, Decimal):
                amount = Decimal(amount)
            if balance + amount < 0:
                return False
            else:
                new_balance = balance + amount
                sql.execute("UPDATE bank_account SET bank_balance=%s WHERE bank_id=%s", [new_balance, bank_id])
                return True


class Transaction(models.Model):
    # to avoid reverse accessor clash, we need to use related_name
    receiver_id = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, related_name='receiver')
    sender_id = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, related_name='sender')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField(auto_now_add=True)

    def createTransaction(sender_id, receiver_id, amount):
        with connection.cursor() as sql:
            sql.execute("SELECT * FROM bank_account WHERE bank_account_number=%s", [sender_id])
            sender = sql.fetchone()
            sql.execute("SELECT * FROM bank_account WHERE bank_account_number=%s", [receiver_id])
            receiver = sql.fetchone()
            if sender is None or receiver is None:
                return False
            if sender[1] >= amount:  # check if sender has enough balance
                sender_bank_id = sender[0]
                receiver_bank_id = receiver[0]
                sql.execute("INSERT INTO transaction (receiver_id, sender_id, amount) VALUES (%s, %s, %s)", [receiver_bank_id, sender_bank_id, amount])

                Bank_Account.updateBalance(sender_bank_id, -amount)
                Bank_Account.updateBalance(receiver_bank_id, amount)
                return True
            else:
                return False

    def getTransactions(c_id):
        with connection.cursor() as sql:
            bank_id = Bank_Account.getBankAccountId(c_id)
            sql.execute("SELECT * FROM transaction WHERE receiver_id=%s OR sender_id=%s", [bank_id, bank_id])
            return sql.fetchall()

    def getFilteredTransactions(c_id, date=None, amount_less_than=None, amount_greater_than=None):
        with connection.cursor() as sql:
            bank_id = Bank_Account.getBankAccountId(c_id)
            query = "SELECT * FROM transaction WHERE (receiver_id=%s OR sender_id=%s)"
            params = [bank_id, bank_id]

            if date:
                query += " AND transaction_date=%s"
                params.append(date)

            if amount_less_than is not None:
                query += " AND amount<%s"
                params.append(amount_less_than)

            if amount_greater_than is not None:
                query += " AND amount>%s"
                params.append(amount_greater_than)
            sql.execute(query, params)
            return sql.fetchall()

