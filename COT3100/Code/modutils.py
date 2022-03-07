# Utilities for modular arithmetic
# Python port 02/22 (just for fun)

# unsigned integer division algorithm 
# a,b (a >= 0, b > 0) --> (q,r), 0 <= r < b and a = q*b + r
def intDivU(a,b) :
    assert a >= 0 and b > 0, "illegal args to unsigned division"
    q = 0
    r = a
    while r >= b :
        q += 1
        r -= b
    return q,r

# signed integer division (reduce to unsigned and adjust)
def intDivS(a,b) :
    assert b != 0, "dividing by zero"
    # make a and b both >= 0
    # case 1: b < 0
    if b < 0 :
        q, r = intDivS(a,-b)    # well, I'm sure you can unfold this recursion SOMEHOW...
        return -q,r
    assert b > 0 # because b != 0
    # case 2: a < 0
    if a < 0 :
        q, r = intDivS(-a,b)
        if r == 0 : return -q,0
        return -q - 1, b - r
    assert a >= 0 and b > 0
    # Now we can use this
    return intDivU(a,b)

# modular addition/multiplication (trivial)
def addMod(a,b,m) :
    return (a + b)%m

def multMod(a,b,m) :
    return (a*b)%m

# Compute (a/b) mod p for prime p 
# We're not testing that 
# USE AT YOUR OWN RISK
def divMod(a,b,p) :
    return multMod(a,modInverse(b,p),p)

# congruence mod m
def congMod(a,b,m) :
    return (a-b)%m == 0

# Just for demonstration - there are better ways to compute that
def expModRec(a,n,m) :
    if n == 0 : return 1
    else      : return (a%m)*expModRec(a,n-1,m) % m

def expModIter(a,n,m) :
    c = 1
    for i in range(1,n) :
        c = (c*a) % m
    return c

# fast (?) algorithm for exponentiation mod m - (b^e) mod m
# fast if the standard exponentiation algorithm
# doesn't use binary templates
# def fastExpMod(x,e,m):
#     X = x
#     E = e
#     Y = 1
#     while E > 0:
#         if E % 2 == 0:
#             X = (X * X) % m
#             E = E/2
#         else:
#             Y = (X * Y) % m
#             E = E - 1
#     return Y

def fastExpMod(x, e, m) :   # Just to make code "portable"
    return pow(x,e,m)       # Well, this thing uses binary templates and is A LOT faster!

# Discrete Logarithm: solve y = a^b mod p for b
# Just try exponentiation with b = 0, 1, 2, 3, ... until it solves
# Only good for small p
def dLog(a,p,y) :
    b = 0
    while fastExpMod(a,b,p) != y : # brute force
        b += 1
    return b

# Euclidean algorithm 
# Don't use this if you don't have to. 
#   It's built into Python
def gcd(a,b) :
    if a == 0 : return b
    if b == 0 : return a 
    return gcd(b%a, a)

def xgcd(a,b) :
    prevx, x = 1, 0; prevy, y = 0, 1
    while b:
        q = a//b
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, a % b
    return a, prevx, prevy

def modInverse(a,m) :
    _, s, _ = xgcd(a,m)
    return s%m

# Just some tests - as usual
if __name__ == '__main__':
    print(intDivS(21,4))
    print(intDivS(-21,-4))
    print(intDivS(-21,4))
    print(intDivS(21,-4))
    #
    print(multMod(3,4,6))
    a = 123
    b = 456
    p = 987
    y = fastExpMod(a,b,p)
    print(y)
    newB = dLog(a,p,y)
    print(newB)
    #
    x = (a*7)%p
    print(x)
    print(modInverse(a,p))
    print(gcd(12,30))       # I said DON'T USE IT!
    print(xgcd(12,30))
    print(xgcd(3,4))
    print(modInverse(3,4))



