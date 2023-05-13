import csv
import datetime

#TODO colorcode statuses?

#TODO handle collisions by chaining
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
        self.timeDelivery = None
        self.timeDepart = None

    def __str__(self):
        print(f"{self.pkgID:^10}{self.pkgAddress:^40}{self.pkgCity:^20}{self.pkgState:^10}{self.pkgZip:^10}{self.pkgWeight:^10}{str(self.timeDepart):^15}{str(self.pkgStatus):^15}{str(self.timeDelivery):^20}{self.pkgDeadline:^10}", end = "  ")
        return ""

    def checkStatus(self, deltaTime):
        if deltaTime > self.timeDelivery:
            self.pkgStatus = "Delivered!"
        elif deltaTime < self.timeDepart:
            self.pkgStatus = "En route!"
        else: 
            self.pkgStatus = "At the hub!"
                     
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
            pkgStatus = None

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
        nextAddressTime = 2000
        nextPackage = None
        for package in unvisited:
            if distanceBetween(getAddress(truck.currentAddress), getAddress(package.pkgAddress)) <= nextAddressTime:
                nextAddressTime = distanceBetween(getAddress(truck.currentAddress), getAddress(package.pkgAddress))
                nextPackage = package
                
        truck.pkgInventory.append(nextPackage.pkgID)
        
        unvisited.remove(nextPackage)
        

        truck.mileage += nextAddressTime
        
        truck.currentAddress = nextPackage.pkgAddress
        
        truck.timeCurrent += datetime.timedelta(hours=nextAddressTime / 18) #18mph speed
        nextPackage.timeDelivery = truck.timeCurrent
        nextPackage.timeDepart = truck.timeDepart
        print(f"Package {nextPackage.pkgID} delivered on {truck.timeCurrent} at {nextPackage.pkgAddress}") #DEBUG
    print(f"packages for truck = {truck.pkgInventory}")
            
            
pkgHashmap = CreateHashmap(40)
loadPackageData(pkgHashmap)
loadDistanceData(distanceData)
loadAddressData(addressData)

truck1 = Truck(18, 0, [15,14,13,16,20,19,17,29,30,31,34,37], '4001 South 700 East', datetime.timedelta(hours=8))
truck2 = Truck(18, 0, [2,3,4,5,7,8,9,10,11,12,18,21,22,23,24,36,38], '4001 South 700 East', datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(18, 0, [1,6,25,26,27,28,32,33,35,39,40], '4001 South 700 East', datetime.timedelta(hours=9, minutes=5)) # packages dont arrive until 905AM


def menu():
    print("\n1. Print All Package Status and Total Mileage")
    print("2. Get a Single Package Status with a Time")
    print("3. Get All Package Status with a Time ")
    print("4. Exit the Program")

def printHeaders():
    print("=" * 160)
    print(f"{'|ID|':^10}{'|Address|':^40}{'|City|':^20}{'|State|':^10}{'|Zip|':^10}{'|Weight|':^10}{'|Time Departed|':^15}{'|Status|':^15}{'|Time Delivered|':^20}{'|Deadline|':^10}")
    print("=" * 160)

# TODO wait for truck 1 to come back so truck 2 can go
truckDeliverPackages(truck1)
truckDeliverPackages(truck2)
truckDeliverPackages(truck3)

selection = 0
while selection != '4':
    menu()
    selection = input("Select an option: ")
    if selection == '1':
        print(f"Total mileage for the route: {truck1.mileage + truck2.mileage + truck3.mileage}")
        printHeaders()
        # End of day time is 5PM
        timeEOD = datetime.timedelta(hours=17)

        for packageID in range(1,41):
            pkg = pkgHashmap.searchKey(packageID)
            pkg.checkStatus(timeEOD)
            print(pkg)

    elif selection == '2':
        time = input("Please enter time in HH:MM:SS format: ")
        (h, m, s) = time.split(":")
        time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        
        pkgID = input("Please enter a package ID: ")
        package = pkgHashmap.searchKey(int(pkgID))
        package.checkStatus(time)

        print("")
        printHeaders()
        print(package)

    elif selection == '3':
        time = input("Please enter time in HH:MM:SS format: ")
        (h, m, s) = time.split(":")
        time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        printHeaders()
        for packageID in range(1,41):
            pkg = pkgHashmap.searchKey(packageID)
            pkg.checkStatus(time)  
            print(pkg)
    elif selection == '4':
        print("Exiting program.")
        exit()



