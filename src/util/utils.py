'''
Created on May 3, 2011

@author: hussein
'''
from paillier import Paillier

def make_vote(base, choice, public_key):  
    vote = base**(choice-1)
    return Paillier.encrypt(vote, public_key)

def str_to_key(str_key):
    key = str_key.split("#")
    return {'n':int(key[0]), 'g':int(key[1])}