import csv

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
    
    def deleteKey(self, key):
        hash = self.hasher
        self.array[hash] = None

class Package:
    def __init__(self, id, address, city, state, zip, deadline, mass, notes = None): 
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes 

    
#read Package csv
# import to Package()
with open("WGUPS Package File.csv") as csvFile:
    read = csv.reader(csvFile)
    for line in read:
        print(line)