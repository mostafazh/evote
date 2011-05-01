'''
Created on Apr 29, 2011

@author: hussein
'''
from MySQLdb import OperationalError, IntegrityError, connect
import hashlib
from util.sendmail import mail
from random import randint

try:
    conn = connect(host="127.0.0.1", user="root", passwd="123456", db="evote")
    conn.autocommit(True)
    curs = conn.cursor()
except OperationalError:
    print "Please check the Database connection"
    exit()
class User:
    
    def __init__(self, id, email):
        self.id = id
        self.email = email  
    
    def login(email, password):
        pass
    login = staticmethod(login)
    
    def register(email, password):
        username = email.split("@")[0]
        
        hasher = hashlib.new('sha1')
        hasher.update(password)
        passhash = hasher.hexdigest()
        
        hasher2 = hashlib.new('md5')
        hasher2.update(randint(5000,1000000))
        randhash = hasher2.hexdigest()
        try:
            curs.execute("INSERT INTO user (email, username, password, vcode) VALUES ('%s', '%s', '%s', '%s')"
                        %(email, username, passhash, randhash))
        except IntegrityError:
            pass
        mail(email, "EVote account activation", str(randhash))
    register = staticmethod(register)
    
    def verify(email, code):
        pass
    verify = staticmethod(verify)
    
    def vote(self, poll_id, vote):
        pass
    
    def check_vote(self):
        pass
    
    