
# NFA --> DFA finger exercise (02/2022)
# Another step to getting to know Python
#
# Simple strategy:
#   Build an NFA with start/accept state(s), transitions as nested dictionaries
#   Then run into the standard algorithm and construct a DFA from it
#   Now since a DFA is nothing but a complete NFA with transitions into singletons
#   that's not really complicated - there isn't need for a DFA class, easy peasy!

#   Doesn't do epsilon transitions (yet)

class NFA: # What a great start!
    def __init__(self, transitions = {}):
        self.table = transitions
        self.start = 0
        self.accepting = set()
        self.alphabet = []
        self.openSets = []
        self.closedSets = []

    def __str__(self):
        return "start: %s\ndelta: %s\naccept: %s" % (self.start,self.table,self.accepting)

    def addTransition(self,inState,symbol,outState):
        # The transition table is a dictionary:
        #    State -> Transitions by symbol which are themselves dictionaries:
        #             Symbol -> set of target states
        # Example: {'0': {'a': {'0'}, 'b': {'1', '0'}}, '1': {'a': {'2'}}, '2': {'a': {'2'}}}

        # Almost got it right out of the box! Almost...
        transitions = self.table.get(inState,None)
        if transitions is None :                # no transitions out of inState so far
            transitions = {}        
            self.table[inState] = transitions   # store empty dictionary
        targets = transitions.get(symbol,None)  
        if targets is None :                    # no transition with this symbol yet
            targets = set()
            transitions[symbol] = targets       # store empty set
        targets.add(outState)                   # add target state

    # Make sure to get the state set from "state" under "symbol"
    # Make it the empty set if there isn't any transition
    def fromState(self,state,symbol):
        transitions = self.table.get(state,None)
        if transitions is None : return set()
        return transitions.get(symbol,set())

    # This is the work horse - and it's so simple
    # Run over all states in the set and union the results with "symbol"
    # Love the set ops in Python, but does this all really scale??
    def fromSet(self,stateSet,symbol):
        result = set()
        for state in stateSet :
            result = result.union(self.fromState(state,symbol))
        return result

    # "ad hoc hack" 
    # it just takes a set of strings, places them in a list
    # sorts them (probably lexicographically, but it really doesn't matter)
    # and then builds a new string from that
    # Why sort? To make this unique for sets (sequence is not determined)
    # shortcut({'a','b','c'}) = shortcut({'b','a','c'}) = 'abc'
    @classmethod
    def shortcut(cls,aSet) :
        strList = []            # I sure can explain all this
        for s in aSet :         # But do I need to?
            strList.append(s)
        strList.sort()
        s = ''                  # Ok, maybe "join" could have done this
        for c in strList :
            s = s + c
        return s

    # Returns a DFA (instance of NFA, just with singleton targets)
    # equivalent to "self" - use the algorithm we all learned to hate
    def toDFA(self) : 
        dfa = NFA({})     # confusing, but sensible, if you know your stuff
        startSet = set(self.start)
        dfa.start = NFA.shortcut(startSet)
        dfa.alphabet = self.alphabet
        
        # Ok, this is how it goes:
        # We have an open list that has the start state set in it
        # Then (in the loop) we take the first element out
        #  Put in the closed list, so we know it's done
        #  Check for each symbol all the transitions out of the set
        #  For each of them check if we already dealt with it
        #  If not, queue it in and continue until we worked them all
        self.openSets = [ startSet ]    # Open list (waiting to be processed)
        self.closedSets = []            # Closed list (processed)

        # work over all upcoming state sets in FIFO fashion
        # you can do LIFO, if you want - doesn't really matter        
        while self.openSets :                       # loop over open list as a queue
            current = self.openSets.pop(0)          # top element, is also removed
            self.closedSets.append(current)         # mark as processed
                                                    # need to do that to avoid duplicates
            stateName = NFA.shortcut(current)       # converts set --> string
                                                    # should have called it "goedelize" 
            # check for acceptance
            if current.intersection(self.accepting) :
                dfa.accepting.add(stateName)

            # for each alphabet symbol
            # compute transitions from current set                                          
            for sym in self.alphabet :
                targets = self.fromSet(current,sym) # compute reachable states with this symbol
                targetName = NFA.shortcut(targets)
                dfa.addTransition(stateName, sym, targetName)

                # check if it's a new target set (not closed)
                # mark for process later by appending it
                if targets not in self.closedSets : 
                    self.openSets.append(targets)  # 'push' if you want LIFO   
                    
        # Ta-DAHHHHHH!                    
        return dfa

if __name__ == '__main__':
    n = NFA()
    n.start = '0'
    n.alphabet = ['a', 'b']

    n.addTransition('0','a','0')
    n.addTransition('0','b','0')
    n.addTransition('0','b','1')
    n.addTransition('1','a','2')
    n.addTransition('2','a','2')
    n.accepting = {'2'}
    print(n)

    dfa = n.toDFA()
    print(dfa)

    # Shouldn't do a thing
    print(dfa.toDFA()) 
