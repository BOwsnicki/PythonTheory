# Utilities for prime sieving
# Python port 02/22 (just for fun)

import primes
from math import sqrt

# Extract the first element of "primes" that divides n
# If that IS a list of primes and it finds a divisor,
# then it finds a prime factor of n - BUT ONLY THEN!
def primeFactor(n,primes) :
    lim = (int)(sqrt(n))           
    index = 0
    while primes[index] <= lim :         # brute force trial division by primes
            if n%primes[index] == 0 :
                return primes[index]    # got one!
            index += 1
    return n                            # looks prime - maybe we rean out of trial primes

def allFactors(n,primes) :
    result = []
    while n != 1 :
        p = primeFactor(n,primes)       # terrible: always starts primes from the beginning
        if p == 1 :
            break
        result.append(p)                # also terrible: no idea how long append takes!
        n = (int)(n/p)
    return result

if __name__ == '__main__':
    primes = primes.sieve(50000)        # grab the primes for this session
    k = 2*3*3*5*7*13*13
    print(allFactors(k,primes))