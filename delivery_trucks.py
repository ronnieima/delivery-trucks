class Hashmap:
    def __init__(self, arraySize):
        self.arraySize = arraySize
        self.array = [None] * arraySize

    #hash formula: (ASCII value of character * 2) % size of the array
    def hasher(self, key):
        hash = 0
        for char in key:
            hash += ord(char) * 2
        return hash % self.arraySize

    def addKVPair(self, key, value):
        hash = self.hasher(key)
        self.array[hash] = value

    def searchKey(self, key):
        hash = self.hasher(key)
        return self.array[hash]



