# Diffie-Hellman breaker
# Python port 02/22 (just for fun)

from modutils import fastExpMod, dLog

# Key Exchange (Diffie-Hellman)

# Alice and Bob publicly agree to use numbers p = 23 and g = 5.

# Alice: chooses secret integer a = 4, sends Bob 		A = g^a mod p: 625 mod 23 = 4
# Bob:	 chooses secret integer b = 3, sends Alice 		B = g^b mod p: 125 mod 23 = 10
# Alice: computes s = B^a mod p = 10000 mod 23 = 18	    â†� Shared secret
# Bob:	 computes s = A^b mod p = 64 mod 23 = 18

# Eavesdropper can only hear g, p, A, B:
# 1. Solve (for b) the discrete log problem B = g^b mod p (symmetric for A = g^a mod p)
# 2. Compute A^b mod p with the b you just found

def breakDH(g,p,A,B) :
    return fastExpMod(A,dLog(g,p,B),p)

if __name__ == '__main__':
    print(breakDH(5,23,4,10))