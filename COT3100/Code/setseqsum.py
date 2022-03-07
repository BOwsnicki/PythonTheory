import unittest 
from functools import reduce

# Python Port 02/2022 Bernd OK

# Now Python has pretty decent sets,
# but sets aren't hashable themselves 
# So there are no such things as sets of sets
# That's particularly weird if you want to do powersets
# So we need a workaround over lists or something like that

def is_empty(a):
    return not a

def powerSet(s) :                 # Now we let this be and return a LIST
                                  # of the subsets of s - as close as we can get
    if is_empty(s) :                
        return [[]]
    
    sCopy = s.copy()
    firstS = sCopy[0]               # First element of the list
    sCopy.remove(firstS)            # The rest
    
    recursivePS = powerSet(sCopy)   # YAY! Finally recursion
    result = []
    for subset in recursivePS :
        result.append(subset)
        withFirst = [ firstS ] + subset.copy()
        result.append(withFirst)
    return result

def cartProd(s1,s2) :
    result = []
    for a in s1 :
        for b in s2 :
            result.append([a,b])
    return result

def sequence(start,end,formula):
    # Now map returns an "iterator" which is pretty smart, if you think about it
    # Here I want a list (just for the heck of it)
    # So I just listify the iterator
    return list(map(formula,range(start,end)))  


# a_n for an arithmetic sequence starting with "aStart"
# and difference d
# We need to specify the index of aStart to make it work

def arith(aStart,start,d,n):
    assert start <= n, "Can't do that backwards"
    # for start = 0 it's just aStart + n*d
    # So, adjust for other values of "start"
    # 0: aStart + n*d
    # 1: aStart + (n-1)*d
    # --> General: 
    return aStart + (n - start)*d

# a_n for a geometric sequence starting with "aStart"
# and ratio r
# We need to specify the index of aStart to make it work

def geom(aStart,start,r,n):
    assert start <= n, "Can't do that backwards"
    # for start = 0 it's just aStart*(r^n)
    # So, adjust for other values of "start"
    # 0: aStart*(r^n)
    # 1: aStart*(r^(n-1))
    # --> General: 
    return aStart*(r**(n-start)) # ** is power in Python

# ##########################################################
# Based on the idea of successive (shorter) sequences
# of differences of the original sequence

# See Mathologer: Why don't they teach Newton's calculus of 'What comes next?'
# https://www.youtube.com/watch?v=4AuV93LOPcE

# Stopping on a constant sequence which can be tested, of course (-> allEqual)

# A quote from Mathologer is important (video at 20:07)
# "The whole 'What's Next' game is fundamentally very silly.
#  If anything can be an answer then of course nothing is an answer"

# Oh, and stop watching at 22:06
# This is higher-end math, enormously pretty, 
# but not really relevant for this course...

def extend(l) :
    assert len(l) > 0, "Can't continue empty list"
    if allEqual(l) :
        result = l.copy()
        result.append(l[0])
        return result
    lenL = len(l)
    
    # len(l) > 1 from here
    
    # a. build list of successive differences
    diffList = []
    for index in range(1,lenL) :
        diffList.append(l[index] - l[index-1])
    # b. extend this by 1 (RECURSION!)
    diffList = extend(diffList)
    
    # c. use the last element of the extended
    #    difference list to extend the original
    result = l.copy()
    result.append(l[lenL - 1] + diffList[lenL - 1])
    return result
# ##########################################################    

# ##########################################################    
# Functional tricks

# If you never looked into Functional Programming: Good luck!

def allEqual(l) :
    return reduce(lambda a,b: a and (b == l[0]),l,True)

def doTimes(f,arg,n) :
    if n == 0: return arg
    return doTimes(f,f(arg),n-1)

# ##########################################################    
# Summation thingies    
# ##########################################################    

def sumUp(start,end,formula):
    return reduce(lambda a,b : a+b, sequence(start, end, formula))

# Closed formulas for arithmetic and geometric sums
#
def sumArith1(start,d,n) :
    return ((n+1)/2)*(start + (start + n*d)) 

def sumArith(start,d,n,startIndex) :
    return sumArith1(start,d,n-startIndex)

def sumGeom1(start,r,n) :
    # Since r can be a floating point, don't ever compare
    # it to zero without a "zero" interval - here it's 1e-6 (ymmv)
    if abs(r-1.0) < 1e-6 : return (n + 1)*start
    return start*(1 - r**(n+1))/(1 - r)

def sumGeom(start,r,n,startIndex) :
    return sumGeom1(start,r,n-startIndex)


def sumLinears(n) :
    return (n*(n + 1)/2)

def sumSquares(n) :
    return (n*(n + 1)*(2*n + 1)/6)

def sumCubes(n) :
    return (n**2*(n + 1)**2/4)

# ########################################################## 
# ########################################################## 
# Unit tests: Not a lot going on   
# ########################################################## 
# ##########################################################    

class TestSum(unittest.TestCase):

    def test_sets(self):
        self.assertEqual(cartProd(['a','b','c'],[0,1]),[['a', 0], ['a', 1], ['b', 0], ['b', 1], ['c', 0], ['c', 1]],
             "Sets 1: [['a', 0], ['a', 1], ['b', 0], ['b', 1], ['c', 0], ['c', 1]] expected")
        self.assertEqual(powerSet([]), [[]], "Sets 2: [[]] expected")
        # That's cheating! I cut and pasted the result into this
        # Reason: The sequence of elements isn't really predictable
        #         but since the lists stand for sets it also doesn't matter
        self.assertEqual(powerSet([1,2]), [[], [1], [2], [1, 2]], "Sets 3:[[], [1], [2], [1, 2]] expected")

    # Just test closed formulas - rest is pretty irrelevant
    def test_sequences(self):
        self.assertEqual(arith(7,1,5,100),502, "Sequences 1: 502 expected")
        self.assertEqual(geom(1,0,2,4),16, "Sequences 2: 16 expected")
        self.assertEqual(geom(1,0,0.5,4),0.0625, "Sequences 3: 0.0625 expected")
        

    def test_functionals(self):
        self.assertTrue(allEqual([1]), "Functionals 1: [1] is allEqual")
        self.assertTrue(allEqual([3,3,3]), "Functionals 2: [3,3,3] is allEqual")
        self.assertFalse(allEqual([3,3,1]), "Functionals 3: [3,3,1] isn't allEqual")
        self.assertEqual(doTimes(lambda a: 2*a, 1, 3),8, "Functionals 4: 8 expected")

    def test_extends(self):
        self.assertEqual(extend([1,2,3]), [1,2,3,4], "Extends 1: [1,2,3,4] expected")
        self.assertEqual(extend([1,-1,-3]), [1,-1,-3,-5], "Extends 2: [1,-1,-3,-5] expected")
        self.assertEqual(extend([1,2,4,8,16]), [1,2,4,8,16,31], "Extends 3: [1,2,4,8,16,31] expected")
        
    def test_sums(self):
        self.assertEqual(sumArith(1,1,100,1), 5050, "Sums 1: Little C.F.G. did better!")
        self.assertEqual(sumGeom(1,1,10,0), 11, "Sums 2: 11 expected")
        self.assertEqual(sumGeom(1,2,10,0), 2047, "Sums 3: 2047 expected")


#######################################################################
#######################################################################
# All demos moved from main here
#######################################################################
#######################################################################
def demos() :
        print(powerSet(['a','b','c']))
        print(cartProd(['a','b','c'],[0,1]))
        print(sequence(0,10,lambda n : 1/(2**n)))
        print(sumUp(0,50,lambda n : 1/(2**n)))
    
        print(arith(7,1,5,100))
        print(geom(1,0,2,4))
        print(geom(1,0,0.5,4))

        print(extend([0,1,2,3,4,5]))
        print(extend([0,1,2,3,4,5,-300])) # That's cute!
        print(extend([0,1,4,9,16,25]))
        print(extend([0,1,8,27,64,125]))
        
        # video at 21:11
        print(extend([1,2,4,8,16]))
        print(extend([1,2,4,8,16,31]))
    
        # functional trickery!
        print(doTimes(extend,[1,2,4,8,16,31],5))

        print(sequence(0,15,lambda n : n**3))
        print(extend(sequence(0,15,lambda n : n**3)))
        print(sequence(0,15,lambda n : 3*n*(n+1)+1))
        print(extend([0,1,8,27,64,125,216]))

        print(extend([0,1,4,9,16,25,36,49]))
        print(extend([0,1,8,27,64,125,216]))
    
        print(extend([1,2,4,8,16,32,64,128,256]))

        print(sumArith(1,1,100,1))
        print(sumGeom(1,2,10,0))

# ########################################################## 
# ##########################################################      
#
if __name__ == '__main__':
    # This has some inactive demos and at the end
    # a more than miserable unit test run
    # demos()
    unittest.main()
