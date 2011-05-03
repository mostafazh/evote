'''
Created on Apr 29, 2011

@author: hussein
'''
from MySQLdb import OperationalError, connect, cursors
from util.paillier import Paillier
from util.utils import str_to_key
from math import log, floor, ceil
from datetime import date, datetime

try:
    conn = connect(host="127.0.0.1", user="root", passwd="123456", db="evote", cursorclass=cursors.DictCursor)
    conn.autocommit(True)
    curs = conn.cursor()
except OperationalError:
    print "Please check the Database connection"
    exit()
    
class Poll:
    
    def __init__(self, id, name, description, created, ends, base, state, public_key, choices, private_key):
        self.id = id
        self.name = name
        self.description = description
        self.created = created
        self.ends = ends
        self.base = base
        self.choices_num = len(choices)
        self.state = state
        self.public_key = public_key
        self.choices = choices
        self.private_key = private_key
        
        
    def flush(self):
        curs.execute("""UPDATE poll 
                        SET name='%s', description='%s', ends='%s', choices_num=%s, state='%s' 
                        WHERE poll_id=%s"""
                        % (self.name, self.description, self.ends, len(self.choices), self.state, self.id))
    
    
    def create(name, description, ends, max_voters, choices):
        base = max_voters + int(ceil(max_voters/10))
        pal = Paillier(int(floor(log(base*(base**2),2))+4))
        pal.generate_keys()
        public_key = str(pal.public_key['n']) + "#" + str(pal.public_key['g'])
        private_key = str(pal.private_key['n']) + "#" + str(pal.private_key['g'])+ "#" + str(pal.private_key['lam'])
        state = Paillier.encrypt(0, pal.public_key)
        now = datetime.now()
        created = date(now.year, now.month, now.day)
        
        curs.execute("""INSERT INTO poll 
                        (name, description, created, ends, base, choices_num, state, public_key, private_key) 
                        VALUES ('%s', '%s', '%s', '%s', %s, %s, '%s', '%s', '%s')"""
                        % (name, description, created, ends, base, len(choices), state, public_key, private_key))
        poll_id = curs.lastrowid
        
        i = 1
        for choice in choices:
            curs.execute("""INSERT INTO choice 
                            (poll_id, choice_id, choice_value) 
                            VALUES ('%s', '%s', '%s')"""
                            % (poll_id, i, choice))
            i += 1
            
        return Poll(poll_id, name, description, created, ends, base, state, public_key, choices, private_key)
    
    
    def get_by_id(poll_id):        
        curs.execute("""SELECT * 
                        FROM poll 
                        WHERE poll_id=%s"""
                        % (poll_id))
        p = curs.fetchone()
        
        if p == None:
            return "no poll with this id"
        
        curs.execute("""SELECT choice_value 
                        FROM choice 
                        WHERE poll_id=%s""" 
                        % (poll_id))
        result_choices = curs.fetchall()
        
        choices = []
        for choice in result_choices:
            choices.append(choice['choice_value'])
        public_key = str_to_key(p['public_key'])
        
        return Poll(int(p['poll_id']), p['name'], p['description'], p['created'], p['ends'], 
                    int(p['base']), int(p['state']), public_key, choices, p['private_key'])
    
    
    def update_state(self, vote):
        self.state = (self.state * vote) % (self.public_key['n']**2)
        self.flush()
        
        
    def get_result(self, private_key):
        pk = private_key.split("#")
        enc_result = Paillier.decrypt(self.state, {'n':int(pk[0]), 'g':int(pk[1]), 'lam':int(pk[2])})
        return self.update_choices(self.id, self.choices, self.base, int(enc_result))
    
    
    def update_choices(self, poll_id, choices, base, m):
        i = len(choices) - 1
        result = {}
        
        while i >= 0:
            result[choices[i]] = int(m / (base**(i)))
            m = m - result[choices[i]] * (base**(i))
            
            curs.execute("""UPDATE choice 
                            SET choice_result=%s 
                            WHERE poll_id=%s AND choice_id=%s"""
                            % (result[choices[i]], poll_id, i+1))
            i -= 1  
        return result
    
    
    '''Static methods'''
    
    create = staticmethod(create)
    get_by_id = staticmethod(get_by_id)