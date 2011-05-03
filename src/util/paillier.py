'''
Created on Apr 27, 2011

@author: hussein
'''
from gmpy import lcm, gcd, invert, next_prime
from random import randint

class Paillier:

    def __init__(self, key_length):
        self.key_length = key_length
        
    def generate_keys(self):
        self.p = self.rand_prime(self.key_length/2)
        
        while True:
            self.q = self.rand_prime(self.key_length/2)
            if not (self.p == self.q):
                break
            
        self.n = self.p * self.q
        self.nsq = self.n * self.n
        self.lam = lcm(self.p-1, self.q-1)
        
        while True:
            self.g = randint(1, self.nsq)
            if gcd(Paillier.L(pow(self.g, self.lam, self.n), self.n), self.n):
                break
        
        self.public_key = {'n':self.n, 'g':self.g}
        self.private_key = {'n':self.n, 'g':self.g, 'lam':self.lam}
            
    def rand_prime(self, length, in_bits = True):
        if in_bits:
            return next_prime(randint(2**(length-1),(2**length)- 1))
        else:
            return next_prime(randint(10**(length-1), (10**length)-1))

    def L(u, n):
        return (u - 1) / n
    
    def encrypt(m, plk):
        return (pow(plk['g'], m, plk['n']**2) * 
                pow(randint(1, plk['n']), plk['n'], plk['n']**2)) % plk['n']**2
    
    def decrypt(c, prk):
        return (Paillier.L(pow(c, prk['lam'], prk['n']**2), prk['n']) * 
                invert(Paillier.L(pow(prk['g'], prk['lam'], prk['n']**2), prk['n']), prk['n'])) % prk['n']
    
    '''Static methods'''
    L = staticmethod(L)
    encrypt = staticmethod(encrypt)
    decrypt = staticmethod(decrypt)
    