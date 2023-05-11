import csv

class CreateHashmap:
    def __init__(self, arraySize):
        self.arraySize = arraySize
        self.array = [None] * arraySize

    #hash formula: (ASCII value of character * 2) % size of the array
    def hasher(self, key):
        return int(key) % self.arraySize

    def addKVPair(self, key, value):
        hash = self.hasher(key)
        keyValue = [key, value]

        if self.array[hash] is None:
            self.array[hash] = list([keyValue])

    def searchKey(self, key):
        hash = self.hasher(key)
        for KVPair in self.array[hash]:
            if key == KVPair[0]:
                return KVPair[1]
        return None
                     
class Truck:
    def __init__(self, speed, mileage, hasDriver,maxCapacity,pkgCount,pkgInventory,currentAddress):
        self.speed = speed
        self.mileage = mileage
        self.hasDriver = hasDriver
        self.maxCapacity = maxCapacity
        self.pkgCount = pkgCount
        self.pkgInventory = pkgInventory
        self.currentAddress = currentAddress

    def __str__(self):
        return f"TRUCK INFO > Speed: {self.speed} MPH | Mileage: {self.mileage} miles | Has a Driver?: {self.hasDriver} | Max Capacity: {self.maxCapacity} | Package Count: {self.pkgCount} | Current Inventory: {self.pkgInventory} | Weight: {self.pkgWeight} | Address: {self.currentAddress}"

class Package:
    def __init__(self, pkgID, pkgAddress, pkgCity, pkgState, pkgZip, pkgDeadline, pkgWeight, pkgStatus):
        self.pkgID = pkgID
        self.pkgAddress = pkgAddress
        self.pkgCity = pkgCity
        self.pkgState = pkgState
        self.pkgZip = pkgZip
        self.pkgDeadline = pkgDeadline
        self.pkgWeight = pkgWeight
        self.pkgStatus = pkgStatus

    def __str__(self):
        return f"PACKAGE INFO > ID: {self.pkgID} | Address: {self.pkgAddress} | City: {self.pkgCity} | State: {self.pkgState} | Zip: {self.pkgZip} | Deadline: {self.pkgDeadline} | Weight: {self.pkgWeight} | Status: {self.pkgStatus}"

def readPackages(pkgHashmap, pkgFile):
    with open(pkgFile) as packageInfo:
        pkgData = csv.reader(packageInfo)
        next(pkgData)
        for package in pkgData:
            pkgID = int(package[0])
            pkgAddress = package[1]
            pkgCity = package[2]
            pkgState = package[3]
            pkgZip = package[4]
            pkgDeadline = package[5]
            pkgWeight = package[6]
            pkgStatus = 'at the hub'

            pkg = Package(pkgID, pkgAddress, pkgCity, pkgState, pkgZip, pkgDeadline, pkgWeight, pkgStatus)

            pkgHashmap.addKVPair(pkgID, pkg)

# load adjacency matrix with distances
adjMatrix = []
with open("Data\WGUPS Distance Table.csv") as distanceInfo:
    distanceData = csv.reader(distanceInfo)
    next(distanceData)
    for row in distanceData:
        adjMatrix.append(row[2:-1])

# calculates the distance between place x and place y
def calcDistance(x, y):
    distance = adjMatrix[x][y]
    if distance == '':
        distance = adjMatrix[y][x]

    return float(distance)
    
            
with open("Data\Address_File.csv") as addressInfo:
    addressData = csv.reader(addressInfo)
    addressData = list(addressData)

def getAddress(givenAddress):
    for address in addressData:
        if givenAddress == address[2]:
            return int(address[0])

pkgHashmap = CreateHashmap(40)
readPackages(pkgHashmap, "Data\WGUPS Package File.csv")