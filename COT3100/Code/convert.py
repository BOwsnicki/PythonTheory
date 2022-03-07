# Base conversion utilities
# Python port 02/22 (just for fun)

# return char for "digit" in "base" ("digit" is a remainder mod "base")
#    if digit <= 9, it's just the digit as a char
#    else 10 --> 'a', 11 -- 'b', etc
def chr4Digit(digit, base) :
    assert (digit >= 0 and digit < base),"Not a legal digit!"
    if digit <= 9 :
        return chr(ord("0") + digit)        # This looks SOOO much like Pascal!
    else :
        return chr(ord("a") + digit - 10)

# convert int "n" to a string for base "b"
def toBase(n, b) :
    result = ''
    while n >= b :
        result = chr4Digit(n%b,b) + result
        n = int(n/b)
    return chr4Digit(n,b) + result


# the inverse of "chr4Digit"
#    '0' - '9' --> 0 - 9
#    'a' --> 10, 'b' --> 11 etc
def digit4Chr(c, base) :
    if (c >= '0' and c <= '9') :
        return ord(c) - ord('0')
    else :
        return ord(c) - ord('a') + 10

# converts a string "s" containing the encoding of an int in base "b" into the value
def fromBase(s, b) :
    result = 0
    factor = 1
    for i in range(len(s)-1, -1, -1) :  # cute way of running backwards through a list!
        result += digit4Chr(s[i],b)*factor
        factor *= b
    return result


# convert string "s" (assuming it's in base "b1") 
# into the string for base "b2"
def changeBase(s,b1,b2) :
    return toBase(fromBase(s,b1),b2)


if __name__ == '__main__':
    print(toBase(255,5))
    print(fromBase('cafe',16))
    print(changeBase('51966',10,16))
    print(changeBase('145376',8,16))
    print(changeBase('cafe',16,19))
