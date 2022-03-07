# Utilities for RSA key pairs
# Python port 02/22 (just for fun)

from key import Key
from primes import sieve, randomPrime
from modutils import fastExpMod, modInverse
from math import gcd                        # the good one!
from factorize import primeFactor

# In case you need a key pair (see demo main)
class KeyPair :

    # that's supposed to be a class variable
    Primes = sieve(50000)

    # initializer with some kind of hand-knit overloading
    #    takes two keys, if one or both not specified, just randomize the pair
    #    if both specified, just store them (that's in case I want special keys for testing)
    def __init__(self, public = None, private = None):
        if public is None or private is None :  # no parameters -->
            self.randomize()                    # just randomize the keys
        else :                                  # keys given -->
            self.public = public                # take those
            self.private = private
        
    # the toString() equivalent
    def __str__(self):
        return "KeyPair\n   public: %s\n   private: %s" % (self.public, self.private)

    def randomize(self):
        # Create a connected random key pair

        # 1. create two different random primes p and q

        # There are practical considerations for selecting these primes
        # a. not too close to the "edges" of the range
        #    too easy to brute-force bidirectionally
        # b. not too close together (close to the center of the range)
        #    too easy to brute-force radially

        # Here we chose to ignore all these considerations :-)

        p = randomPrime(KeyPair.Primes,2)       # don't want the 2
        q = randomPrime(KeyPair.Primes,2)       # ditto
        while (q == p) :                        # and here I would love to use a do-while, but alas...
            q = randomPrime(KeyPair.Primes)     # shouldn't dead loop, right?

        # 2. Modulus and totient
        n = p*q                                 # modulus
        phi = (p - 1)*(q - 1)                   # totient

        # 3. e must be relatively prime to phi
        #    else modInverse won't work
        e = 65537                               # usually a good guess
        while gcd(e,phi) != 1 :                 # just in case - never seen this loop run
            e += 2                              # since (p-1)*(q-1) is even, e better be odd

        # 4. d solves e^d = 1 (mod phi)
        d = modInverse(e,phi)

        # Got it
        self.public = Key(n,e)
        self.private = Key(n,d)

    # encryption (Who would've thought...)
    def encrypt(self,m) :
        return fastExpMod(m,self.public.second,self.public.first)

    # decryption (Why am I even writing these stupid comments??)
    def decrypt(self,c) :
        return fastExpMod(c,self.private.second,self.private.first)



if __name__ == '__main__':
     
    pair = KeyPair()            # This is how you set up a random key pair here
                                # There's another version of this initializer
                                #    KeyPair(key1,key2) like KeyPair(Key(12,22), Key(200,300))
                                # that does NOT randomize the keys,
                                # in case I have two specific keys I want to test
    print(pair)

    # encrypt and decrypt (just for fun)
    m = 1776
    c = pair.encrypt(m)
    print("message",m,"encrypted",c,"decrypted",pair.decrypt(c))

    #############################################################################
    # Now break it
    #############################################################################
    n = pair.public.first   # Just based on the public key
    e = pair.public.second

    # 1. Factor n into p and q
    p = primeFactor(n,KeyPair.Primes)
    q = n//p
    print("factored:",n,"=",p,"*",q)

    # 2. Use code from randomize to compute d (should be = pair.private.second)
    phi = (p-1)*(q-1)
    d = modInverse(e,phi)

    # 3. Decrypt with d and n
    print("broken: ",d,fastExpMod(c,d,n))

