'''
Created on Apr 29, 2011

@author: hussein
'''
from MySQLdb import OperationalError, IntegrityError, connect, cursors
import hashlib
from util.sendmail import mail
from random import randint
from poll import Poll

try:
    conn = connect(host="127.0.0.1", user="root", passwd="123456", db="evote", cursorclass=cursors.DictCursor)
    conn.autocommit(True)
    curs = conn.cursor()
except OperationalError:
    print "Please check the Database connection"
    exit()
    
class User:
    
    def __init__(self, id, username, email, is_verified, is_admin):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.is_verified = is_verified
        
    def flush(self):
        curs.execute("""UPDATE user 
                        SET username='%s', email='%s', is_verified=%s, is_admin=%s
                        WHERE user_id=%s"""
                        % (self.username, self.email, self.is_verified, self.is_admin, self.id))
    
    
    def login(email, password):
        pass
    
    
    def register(email, password):
        username = email.split("@")[0]
        
        hasher = hashlib.new('sha1')
        hasher.update(password)
        passhash = hasher.hexdigest()
        
        hasher2 = hashlib.new('md5')
        hasher2.update(`randint(5000,1000000)`)
        randhash = hasher2.hexdigest()
        
        try:
            curs.execute("""INSERT INTO user 
                            (email, username, password, vcode) 
                            VALUES ('%s', '%s', '%s', '%s')"""
                            % (email, username, passhash, randhash))
        except IntegrityError:
            return "user with same email exists."
        
        curs.lastrowid
        mail(email, "EVote account activation", str(randhash))
        return "good"
    
    
    def get_by_id(id):
        curs.execute("""SELECT username, email, is_admin, is_verified 
                        FROM user 
                        WHERE user_id=%s"""
                        % (id))
        row = curs.fetchone()
        
        if row == None:
            return "no user with this id"
        return User(id, row['username'], row['email'], row['is_verified'], row['is_admin'])
    
    
    def verify(email, code):
        curs.execute("""SELECT user_id, username, email, vcode, is_admin, is_verified 
                        FROM user 
                        WHERE email='%s'"""
                        % (email))
        row = curs.fetchone()
        
        if row == None:
            return "no user with this email"
        elif not row['vcode'] == code:
            return "verification code is wrong"
        
        user = User(row['user_id'], row['username'], row['email'], 1, row['is_admin'])
        user.flush()
        return user
    
    
    def vote(self, poll_id, vote):
        try:
            curs.execute("""INSERT INTO vote 
                            (poll_id, user_id, value) 
                            VALUES (%s, %s, '%s')"""
                            % (poll_id, self.id, vote))
        
        except IntegrityError:
            return "user voted befor"
        
        poll = Poll.get_by_id(poll_id)
        poll.update_state(vote)
        return "good"
    
    
    def check_vote(self):
        pass
    
    
    '''Static methods'''
    
    login = staticmethod(login)
    register = staticmethod(register)
    get_by_id = staticmethod(get_by_id)
    verify = staticmethod(verify)