class Hashmap:
    def __init__(self, arrSize):
        self.arrSize = arrSize
        self.array = [None] * arrSize

    #hash formula: (ASCII value of character * 2) % size of the array
    def hasher(self, key):
        hash = 0
        for char in key:
            hash += ord(char) * 2
        return hash % self.arrSize




