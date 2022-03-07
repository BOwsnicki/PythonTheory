# Utilities for RSA keys
# Python port 02/22 (just for fun)

# Just a container with str function
class Key:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return "Key [first: %d, second: %d]" % (self.first, self.second)   

if __name__ == '__main__':
    key = Key(111,-7)
    print(key)