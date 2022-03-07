from abc import ABC

# or(impl(p,q),impl(q,p))
# Syntax:
# Expr --> Variable | Constant | Op ( Expr ) | Op ( Expr , Expr )
# Variable --> p, q, r, s, t
# Constant --> T | F
# Op --> and | or | impl | not

# Strategy:
#    Parse with Recursive Descent into op tree
#    Create environments for occurring variables
#    Evaluate the tree for each environment

#
# Ok, here we go!
#

# Abstract Node class
#    Not sure how good this idea is, looks like overkill
#    Anyway: We have two Node types: Inner and Leaf
#    Both have a "Label" and "Data"
#    Inner also has a successor list
#        Could have been just "Left" and "Right" but that's more general
#        Just make sure the sequence is right if the op isn't commutative!
#    Labels for inner nodes: 'LogOp1' and 'LogOp2'
#    Labels for leaves: 'const' and 'var'
#    Data for inner nodes: Name of the op, such as "and", "not", ...
#    Data for leaves: constant value or variable name
#
#    Try this with static typing, just saying!


class Node(ABC) :               # ABC = Abstract Base Class
    def __init__(self, label) :
        self.label = label
        self.data = None

    # Printing these things isn't really easy with all the
    # indentation needed. Also, the confusion about "str" and
    # "rep" in Python isn't helping - so take this as a sketch!
    
    def __str__(self):
        return "Node :label %s data %s"  % (self.label, self.data)

    def __repr__(self):
        return self.__str__()


# Inner nodes also have a successor list and an addSucc method    

class InnerNode(Node) :
    def __init__(self, label) :
        Node.__init__(self, label)
        self.succ = []
    
    def __str__(self):
        return "Node :label %s data %s\n succ %s"  % (self.label, self.data, self.succ)
    
    def addSucc(self, s) : # Add a successor (Don't look so surprised!)
        self.succ.append(s) 


# And here is where it becomes shady:
#    Actually, the class "Node" does everything a Leaf needs to do
#    But do we really make InnerNode a flippin' subclass of LeafNode?
#    Because now a LeafNode doesn't do anything different from its superclass Node

class LeafNode(Node) : pass

# A Parser does what parsers do: Parse with Recursive Descent
# Now it also contains a Scanner - no need to make them different

# A Scanner does what scanners do: Just deliver the tokens 
# in the source code one-by-one (check section A below for use)
# It needs the "source" (a string) and a dictionary "table"
# "table" contains pairs text : token, where "text" is the literal
# appearance of the token in the source and "token" is the token class
# Also see the example below
 
class Parser :
    def __init__(self, source, table) :
        self.source = source
        self.table = table

        # Initialize Scanner state
        self.position = 0           # First character
        self.currentText = None     # Current text/token
        self.currentToken = None    # Nothing beats good naming, right?
        
        self.variables = []         # Extracted variables, no duplicates
                                    # Easier to extract during scanning

    # Return class and text of the next token
    # 'eoI' is artificial and denotes "End of Input"
    # 'Unknown' is a class for text that doesn't translate into a proper token
    # Lots of assumptions in this, needs to be rewritten if
    #    a) we have numerical constants
    #    b) we have alphanumerical variable names
    #    c) it's Monday
    
    def nextToken(self) :
        if self.position >= len(self.source) :
            return 'eoI', 'eoI'                 # Done! Both are the same
        
        text = ''                               # Accumulates the text
        c = self.source[self.position]
        if not c.isalpha() : # that's for '(', ')' and ','
            text += c
            self.position += 1  # only one char
        else :
            # Collect alpha string, works for ops, vars and consts
            while c.isalpha() : 
                text += c
                self.position += 1
                c = self.source[self.position]
        
        # Got the token text, look up the class in the dictionary and call it quits
        # 'Unknown' is default return from the dictionary if it's not found

        self.currentText, self.currentToken = text, self.table.get(text,'Unknown')
        return self.currentToken, self.currentText

    # Aux method to assert that "token" is the current one 
    # Great for delimiters, separators, stupid things like "then", ...
    # No recovery if it doesn't match, lousy error handling
    # Also I would have liked to call it "match" but that seems to be reserved
    def skip(self,token) :
        if self.currentToken != token :
            print(token + ' expected, found ' + self.currentToken + '(' + self.currentText + ')')
        # "skip" skips forward - This Is The Way!
        return self.nextToken()

    # RD code for "Expr"
    def expr(self) :
        # Standard approach: Check current token and go from there
        # Oh, by the way: The omission of switches in Python is criminal
        if self.currentToken == 'logOp1' :
            # Expr --> Op(Expr)
            # Create inner node for it
            root = InnerNode(self.currentToken)
            root.data = self.currentText
            self.nextToken()            # Ok, ready to go into the argument
            self.skip('oParen')         # Skip (
            root.addSucc(self.expr())   # Place "Expr" arg node as successor
            self.skip('cParen')         # Skip )
            return root

        if self.currentToken == 'logOp2' :  
            # Pretty much the same for 2-place op
            # Expr --> Op(Expr,Expr)
            root = InnerNode(self.currentToken)
            root.data = self.currentText
            self.nextToken()
            self.skip('oParen')         # Skip (
            root.addSucc(self.expr())   # Link in first arg node
            self.skip('comma')          # Skip ,
            root.addSucc(self.expr())   # Link in second arg node
            self.skip('cParen')         # Skip )            
            return root
        
        #  Leaves for vars and constants: Trivial?
        if (self.currentToken == 'var' or self.currentToken == 'const') :
            node = LeafNode(self.currentToken)
            node.data = self.currentText
            
            if self.currentToken == 'var' : # Cheap hack to record variables
                # record variable, if new
                if self.currentText not in self.variables :
                    self.variables.append(self.currentText)

            self.nextToken()    # Make sure you always do that!
            return node
        
        
    # That's easy now: Reset Scanner, skip into first token and do Recursive Descent 
    def parse(self) :
        self.position = 0
        self.currentText = None
        self.currentToken = None
        self.variables = []
        
        self.nextToken()    # Always skip in before parsing!
        return self.expr()  # Dive into Recursive Descent

# This is the framework for evaluating a tree in a given environment
# An environment is just a dictionary with entries var : value
# Pretty easy, tbh I just wrote it to practice Python class methods

class Evaluator :
    
    # A. Simple recursive postfix printer from the expression tree
    @classmethod    
    def postfix(cls,root) :
        if type(root) == LeafNode :
            print(root.label+":",root.data)
        else :
            # Postfix: Left, Right, Root
            cls.postfix(root.succ[0])
            # Jeez! Can you believe I fell into this trap??
            if root.label == 'logOp2' : cls.postfix(root.succ[1])
            print(root.data)

    # Create all environments for a given list of variables
    # Do this recursively, but make sure you make copies!
    
    # We don't really have to sort the variables of course
    # but the way this works is that environments are created
    # via tail recursion, i. e. in reverse... 
    @classmethod    
    def environments(cls,variables):
        varSorted = variables.copy()
        varSorted.sort(reverse=True)
        return cls.environmentsAux(varSorted,0,len(varSorted))
    
    # This is the recursive worker, pretty straight forward
    # create a two-element environment with True/False for 
    # the base case of one variable
    # The base case of no variables is there if we only have constants
    @classmethod       
    def environmentsAux(cls,variables,index,length):
        # Base case 1: No variables --> [{}] = one empty environment
        if index >= length : return [{}]

        # Base case 2: One variable: List with two trivial environments
        vName = variables[index]
        if index == length-1 :
            return [{ vName : True }, { vName : False }]
        
        # Recursion:
        #   Generate environments for the rest of the variables
        #   and create two out of each - for both values of vName
        remaining = cls.environmentsAux(variables, index+1, length)
        result = []
        for env in remaining :      # Easy-ish! Just make sure you have copies
            envCopy1 = env.copy()   # of the recursively generated environments
            envCopy2 = env.copy()   # Not sure if we really need two copies!
            envCopy1[vName] = True  # One with the current variable True
            envCopy2[vName] = False # One with the current variable False
            result.append(envCopy1) # Add the new environments to solution
            result.append(envCopy2)
        return result
    
    # Evaluate a two-place op with the given args
    @classmethod
    def eval2(cls,op2,bool1,bool2):
        if op2 == 'or' : return bool1 or bool2
        if op2 == 'and' : return bool1 and bool2
        if op2 == 'impl' : return (not bool1) or bool2
        if op2 == 'equiv' : return bool1 == bool2
        if op2 == 'nor' : return not (bool1 or bool2)
        if op2 == 'nand' : return not (bool1 and bool2)
        
    
    # Evaluate a one-place op with the given arg
    @classmethod
    def eval1(cls,op1,bool1):
        if op1 == 'not' : return not bool1
    
    # Evaluate a node: Depends on what kind of node
    @classmethod
    def evalNode(cls,node,env):
        # If it's a constant leaf, it's the value (as a bool)
        if (node.label == 'const'): return (node.data == 'True')

        # If it's a variable leaf, look the value up in the environment
        if (node.label == 'var'): return env[node.data]

        # If it's a one-place op, eval the argument and then do the op with the result
        if (node.label == 'logOp1'):
            arg = cls.evalNode(node.succ[0],env)
            return cls.eval1(node.data,arg)

        # If it's a two-place op, eval the arguments and then do the op with the results
        if (node.label == 'logOp2'):
            arg1 = cls.evalNode(node.succ[0],env)
            arg2 = cls.evalNode(node.succ[1],env)
            return cls.eval2(node.data,arg1,arg2)
        

if __name__ == '__main__':

    # Everyone's favorite tautology:
    #     (p --> q) or (q --> p)
    #     Given any two propositions p and q, one implies the other 
    # code = 'or(impl(p,q),impl(q,p))'
    
    #     (p --> q) or (q --> r)
    #     is a pretty terrible generalization
    #     Just look at it! I mean LOOK AT IT!!
    # code = 'or(impl(p,q),impl(q,r))'
    

    # Some more to try?
    # code = 'impl(p,or(q,r))'
    # (p --> q or r) <--> (p --> q) or (p --> r)
    code = 'equiv(impl(p,or(q,r)),or(impl(p,q),impl(p,r)))'
    # DeMorgan:
    # code = 'equiv(not(or(p,q)),and(not(p),not(q)))'
    # code = "equiv(not(and(p,q)),nand(p,q))"
    # code = "equiv(not(and(p,False)),True)"
    # code = "equiv(not(False),True)"
    # code = "not(and(False,True))"
    
# A. Check Scanner part for tokenized code
# A1. Token table (easy!)
    table = {
        '(' : 'oParen',
        ')' : 'cParen',
        'p' : 'var',
        'q' : 'var',
        'r' : 'var',
        's' : 'var',
        't' : 'var',
        'and' : 'logOp2',
        'or' : 'logOp2',
        'impl' : 'logOp2',
        'equiv' : 'logOp2',
        'nor' : 'logOp2',
        'nand' : 'logOp2',
        'not' : 'logOp1',
        ',' : 'comma',
        'True' : 'const',
        'False' : 'const'
    }
    
# A2. Dig in and see what comes out
    p = Parser(code,table)
    tok, text = p.nextToken()
    while tok != 'eoI' :
        print(tok,text)
        tok, text = p.nextToken()


# B. Parse it, look at the op tree and do a postfix print (easier to check)
#    Then check the variables     
    tree = p.parse()
    print(tree)
    print(Evaluator.postfix(tree))
    var = p.variables
    print(var)

# C. Run this tree through the Evaluator by creating all possible
#    bindings (environments) for the variables and evaluating them all
    print(Evaluator.environments(var))
    for env in Evaluator.environments(var) :
        print(env, Evaluator.evalNode(tree,env))
    