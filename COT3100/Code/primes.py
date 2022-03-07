# Utilities for sieving primes
# Python port 02/22 (just for fun)

import random

# Standard Sieve of Eratosthenes

def sieve(n) :
    sieve = [True for i in range(n + 1)]
    p = 2
    while (p * p <= n):        
        # Find next prime - mark all multiples as not prime
        if (sieve[p]) :
            for i in range(p*p, n + 1, p):
                sieve[i] = False
        p += 1

    # Collect/return primes off the sieve
    primes = []
    for p in range(2, n+1):
        if sieve[p] :
            primes.append(p)
    return primes

def randomPrime(primes, start = 1) :
    index = random.randrange(start,len(primes)) - 1
    return primes[index + start - 1]

# Just some tests - as usual
if __name__ == '__main__':
    primes = sieve(50000)
    print(randomPrime(primes))
    print(randomPrime(primes))
    print(randomPrime(primes,2))
    print(randomPrime(primes))
    print(randomPrime(primes))
    print(sieve(500))
