import csv
import datetime

class CreateHashmap:
    def __init__(self, arraySize):
        self.arraySize = arraySize
        self.array = [None] * arraySize

    #hash formula: (sum of ASCII value of each character) % size of the array
    def hasher(self, key):
        return key % self.arraySize

    def addKVPair(self, key, value):
        hash = self.hasher(key)
        keyValue = [key, value]

        if self.array[hash] is None:
            self.array[hash] = list([keyValue])
        else:
            self.array[hash] = [].append(list([keyValue]))

    def searchKey(self, key):
        hash = self.hasher(key)
        for KVPair in self.array[hash]:
            if key == KVPair[0]:
                return KVPair[1]
        return None
    
                     
class Truck:
    def __init__(self, speed, mileage, pkgInventory,currentAddress, timeDepart):
        self.speed = speed
        self.mileage = mileage
        self.pkgInventory = pkgInventory
        self.currentAddress = currentAddress
        self.timeDepart = timeDepart
        self.timeCurrent = self.timeDepart
       
    
    def __str__(self):
        return f"TRUCK INFO > Speed: {self.speed} MPH | Mileage: {self.mileage} miles | Has a Driver?: {self.hasDriver} | Max Capacity: {self.maxCapacity} | Current Inventory: {self.pkgInventory} | Weight: {self.pkgWeight} | Address: {self.currentAddress}"

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

# load adjacency matrix with distances
with open("traveling-salesman\Data\WGUPS Distance Table.csv") as distanceInfo:
    distanceCSV = csv.reader(distanceInfo)
    distanceCSV = list(distanceCSV)

with open("traveling-salesman\Data\Address_File.csv") as addressInfo:
    addressCSV = csv.reader(addressInfo)
    addressCSV = list(addressCSV)

with open("traveling-salesman\Data\WGUPS Package File.csv") as packageInfo:
    packageCSV = csv.reader(packageInfo)
    packageCSV = list(packageCSV)

def loadPackageData(pkgHashmap):
        for package in packageCSV:
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
            
distanceData = []
def loadDistanceData(distanceData):
    for distance in distanceCSV:
        distanceData.append(distance)

addressData = []
def loadAddressData(addressData):
    for address in addressCSV:
        addressData.append(address[2])

def getAddress(givenAddress):
    for address in addressData:
        if givenAddress == address:
            return addressData.index(address)
            
# calculates the distance between place x and place y
def distanceBetween(x, y):
    distance = distanceData[x][y]
    if distance == '':
        distance = distanceData[y][x]
    return float(distance)
    
def minDistanceFrom(fromAddress, truckPackages):
    minDistance = (distanceBetween(fromAddress, getAddress(pkgHashmap.searchKey(truckPackages[0]).pkgAddress)))
    for package in truckPackages:
        toAddress = getAddress(pkgHashmap.searchKey(package).pkgAddress)
        distance = distanceBetween(fromAddress, toAddress)
        if (distance < minDistance):
            minDistance = distance
            minAddress = toAddress
    return minAddress

def truckDeliverPackages(truck: Truck):
    unvisited = []

    for packageID in truck.pkgInventory:
        pkg = pkgHashmap.searchKey(packageID)
        unvisited.append(pkg)

    truck.pkgInventory.clear()

    while len(unvisited) > 0:
        nextAddress = 3000
        nextPackage = None
        for package in unvisited:
            if distanceBetween(getAddress(truck.currentAddress), getAddress(package.pkgAddress)) <= nextAddress:
                nextAddress = distanceBetween(getAddress(truck.currentAddress), getAddress(package.pkgAddress))
                nextPackage = package
                
                truck.pkgInventory.append(nextPackage.pkgID)
                
                unvisited.remove(nextPackage)
                
                truck.mileage += nextAddress
                
                truck.address = nextPackage.pkgAddress
                
                truck.timeCurrent += datetime.timedelta(hours=nextAddress / 18)
                nextPackage.delivery_time = truck.timeCurrent
                nextPackage.departure_time = truck.timeDepart
            
            
    



pkgHashmap = CreateHashmap(40)
loadPackageData(pkgHashmap)
loadDistanceData(distanceData)
loadAddressData(addressData)

truck1 = Truck(18, 0, [1, 2, 4, 5, 7, 8, 10, 11, 12, 13, 36, 17, 19, 21, 22, 23], '4001 South 700 East', datetime.timedelta(hours=8))
truck2 = Truck(18, 0, [9, 14, 16, 38, 19, 20, 24, 26, 27, 29, 30, 31, 33, 3, 18, 15], '4001 South 700 East', datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(18, 0, [6, 34, 25, 28, 32, 35, 37,39, 40], '4001 South 700 East', datetime.timedelta(hours=9, minutes=5)) # packages dont arrive until 905AM


print(truckDeliverPackages(truck1))
print(truckDeliverPackages(truck2))
print(truckDeliverPackages(truck3))



