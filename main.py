#Tyler Johnson 0326099 - WGUC950
import csv;
from datetime import datetime, timedelta

#a = "2010 W 500 S"
#b = "Salt Lake City Streets and Sanitation 2010 W 500 S"
#print(a in b)

#1 - We must create the class & define the structure for the data we will be handling, in this case a Package.
class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, note, status):
        self.id = int(id)
        self.address = str(address)
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status
        self.deliverytime = "NA"
        self.history = []
        self.delivered = False

    def print(self):
        print(self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.note, self.status, self.deliverytime)

    def setDeliveryTime(self, mins):
        hour = "{:02d}".format(int(mins / 60))
        minute = "{:02d}".format(mins % 60)
        time = hour + ':' + minute
        self.deliverytime = time

    def appendHistory(self, time, status):
        if "Delivered" in status:
            self.delivered = True
        self.history.append([time, status])


#test = Package(1, "1234", 12, "Waddell", 85355, 10, 0)
#test.print()

#2 - Next a hash table is created for storing and loading Packages.
class HashTable:
    #O(N)
    def __init__(self, capacity = 10):
        self.capacity = capacity
        self.hashtable = []
        for i in range (capacity):
            self.hashtable.append([])
    #O(1)
    def hash(self, key):
        hash = key % len(self.hashtable)
        return hash
    #O(1)
    def put(self, key, package):
        bucket = self.hash(key)
        self.hashtable[bucket].append(package)
    #O(log n)
    def get(self, key):
        bucket = self.hash(key)
        packages = self.hashtable[bucket]
        #print("Getting " + str(key))
        for package in packages:
            #print("Ids " + str(package.id))
            if package.id == key:
                #print("Found " + str(key))
                index = packages.index(package)
                return packages[index]
    #O(N^2)
    def printTable(self):
        for lists in self.hashtable:
            for entry in lists:
                print(entry.id)
    #O(N^2)
    def printPackageStatuses(self):
        string = ''
        for lists in self.hashtable:
            for entry in lists:
                string += str(entry.id) + " : " + str(entry.status) + " \n"
        return string

    #O(log n)
    def remove(self, key):
        bucket = self.hash(key)
        packages = self.hashtable[bucket]
        for package in packages:
            if package.id == key:
                #print("Removing " + str(key))
                packages.remove(package)


#ht = HashTable()
#ht.put(test)
#out = ht.get(test)
#out.print()

hashtable = HashTable()

#3 Here we must populate the hashtable using the csv files.
#O(N)
#with open('Packages.csv') as file:
#    data = csv.reader(file, delimiter=',')
#    for row in data:
#        hashtable.put(Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'At Hub'))

#4 Create a graph which will be used with distance data and ultimately the algorithm
#6.6 Python:Graphs from zybooks 7.2
class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def addVertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight = 0.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight = 0.0):
        #print("a " + str(vertex_a) + " b " + str(vertex_b))
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def getDistance(self, origin, destination):
        pointa = None
        pointb = None
        for key in graph.adjacency_list.keys():
            if pointa is not None and pointb is not None:
                break
            if origin == key:
                pointa = key
            if destination == key:
                pointb = key
        distance = self.edge_weights[pointa, pointb]
        return distance

#Each point on our map is a vertex on the graph. Each edge is the distance between vertexs
class Vertex:
    def __init__(self, title):
        self.title = title

#5 Next we create a graph object and populate the graph with our distance data
graph = Graph()
distances = []
destinations = []
destanddistances = []
vertexs = []
key = 0;
with open("Distances.csv") as file:
    data = csv.reader(file, delimiter=',')
    for row in data:
        if(data.line_num == 29):
            destinations = row
            destinations.pop(0)
            #for i in range(0, len(destinations)):
            #    destinations[i] = str(destinations[i])
            #for i in range(0, len(destinations)):
                #key = Vertex(destinations[i])
                #print(key + " dsfsdfdsf")
        if(data.line_num != 29):
            #key = row[0]
            #print(key)
            #for i in range(0, 26):
            graph.addVertex(key)
            vertexs.append(key)
            adjacencylist = []
            for i in range(1, 28):
                adjacencylist.append(row[i])
            destanddistances.append((key, adjacencylist))
            #print(adjacencylist)
            graph.adjacency_list[key] = adjacencylist
            key += 1
    for i in range(0, len(destanddistances)):
        edges = list((destanddistances[i])[1:len(destanddistances)][0])
        for j in range(0, len(edges)):
            if edges[j] == "": #or edges[x] == "0.0":
                break
            else:
                a = list(destanddistances[i])[0]
                b = list(destanddistances[j])[0]
                weight = float(edges[j])
                #print(str(i) + " <-----> " + str(x) + " = " + str(weight), end= "   ")
                #print(str(i) + " <-----> " + str(x))
                graph.add_undirected_edge(int(i), int(j), weight)
                #graph.add_undirected_edge(a, b, weight)
#print(destinations)

#6 We now need to create the Trucks for our delivery algorithm
class Truck:
    def __init__(self, name, packages, location, time, printtime):
        self.packages = packages
        #Each truck can carry a maximum of 16 packages,
        self.capacity = 16
        self.name = name
        self.location = location
        #time in minutes
        self.time = time
        #The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
        self.speed = 18
        self.distance = 0
        self.printtime = printtime
        self.printing = True
        self.printpackages = ''

    def addPackage(self, packageid):
        if len(self.packages) <= self.capacity:
            self.packages.append(packageid)
        else:
            print("Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.")

    def printPackages(self):
        print(self.packages)

    def setLocation(self, location):
        self.location = location

    def setTime(self, distance):
        self.time = self.time + timedelta(hours = distance / self.speed)

    # O(N^2)
    def calculateNextPackage(self, curIndex):
        distancetobeat = 99
        next = None
        nextvertex = None
        for i in self.packages:
            package = hashtable.get(i)
            index = 0
            for i in range(0, len(destinations)):
                # The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m.
                # WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m.
                # However, WGUPS does not know the correct address (410 S State St., Salt Lake City, UT 84111) until 10:20 a.m.
                #at this point it's 10:20 and we have the address
                if package.id == 9:
                    package.address = "410 S State S"
                    package.city = "Salt Lake City"
                    package.state = "UT"
                    package.zip = "84111"
                if package.id == 12:
                    package.address = "3575 W Valley Central"
                if package.address in str(destinations[i]):
                    index = i;
                #print("index is " + str(index));
            distance = float(graph.getDistance(vertexs[curIndex], vertexs[index]))
            #print("Distance from " + str(vertexs[curIndex]) + " to " + str(vertexs[index]) +  " is " + str(distance))
            if distance < distancetobeat:
                #print("Distance " + str(distancetobeat) + " was beat by " + str(distance))
                distancetobeat = distance
                next = package
                nextvertex = index
            #print(str(distancetobeat) + " to next " + str(nextvertex))
        return distancetobeat, next, nextvertex

    #O(N^2)
    def calculateTrip(self):
        #Update Package Statuses
        for packageid in self.packages:
            package = hashtable.get(packageid)
            package.status = "en route"
        currentnode = 0 #HUB
        #O(N)
        for i in range(len(self.packages)):
            distance, package, currentnode = self.calculateNextPackage(currentnode)
            #print("current node is " + str(currentnode) + " which is " + str(destinations[currentnode]))
            #print("delivering package " + str(package.id))
            self.incDistance(distance)
            self.deliver(package, distance)
        backToHub = float(graph.getDistance(vertexs[currentnode], vertexs[0]))
        self.incDistance(backToHub)
        self.incTime(backToHub)
        return self.distance

    def deliver(self, package, distance):
        self.incTime(distance)
        #self.distance += distance
        package.setDeliveryTime(self.time)
        package.status = "Delivered at " + package.deliverytime
        self.packages.remove(package.id)

    def incTime(self, distance):
        if self.time > self.printtime and self.printing:
            self.printtime = self.time
            self.printpackages = hashtable.printPackageStatuses()
            self.printing = False
        self.time += int((distance / 18) * 60)
        for i in range (1, 40):
            package = hashtable.get(i)
            if package.delivered == False:
                package.appendHistory(self.time, package.status)

    def incDistance(self, amount):
        self.distance += amount

#There are a lot of notes/requirements for packages and I am unsure of how to navigate this.
#You can write an entirely seperate program for taking package data and assigning trucks
#To save time I will do this somewhat manually
Truck1 = Truck('Truck1', [1, 4, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 37, 39, 40], 'HUB', 480, 515) #8AM
Truck2 = Truck('Truck2', [2, 3, 6, 18, 25, 28, 31, 32, 36, 38], 'HUB', 545, 575) #will not arrive to depot until 9:05 but deadline 10:30
Truck3 = Truck('Truck3', [5, 7, 8, 9, 10, 11, 12, 17, 22, 23, 24, 26, 27, 33, 35], 'HUB', 620, 723)

with open('Packages.csv') as file:
    data = csv.reader(file, delimiter=',')
    for row in data:
        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'At Hub')
        #destinations.append()
        #package.print()
        hashtable.put(int (package.id), package)
        #print(package.id)
        #print(package.id in str(set1))
        #for i in set1:
            #print(int(i))
        #    if int(i) == int(package.id):
        #        Truck1.addPackage(package)
        #for i in set2:
        #    if int(i) == int(package.id):
        #        Truck2.addPackage(package)
        #for i in set3:
        #    if int(i) == int(package.id):
        #        Truck3.addPackage(package)

#Truck1.printPackages()
#Truck2.printPackages()
#Truck3.printPackages()

#hashtable.printTable()
distance1 = Truck1.calculateTrip()
distance2 = Truck2.calculateTrip()
distance3 = Truck3.calculateTrip()

#hashtable.printPackageStatuses()

message = '''
WGUC950 Commands:
q = quit
1-40 = Package ID for Package Info
A = Provide screenshots to show the status of all packages at a time between 8:35 a.m. and 9:25 a.m.
B = Provide screenshots to show the status of all packages at a time between 9:35 a.m. and 10:25 a.m.
C = Provide screenshots to show the status of all packages at a time between 12:03 p.m. and 1:12 p.m.
H = Total Mileage By All Trucks
'''
def minutesToTime(mins):
    hour = "{:02d}".format(int(mins / 60))
    minute = "{:02d}".format(mins % 60)
    time = hour + ':' + minute
    return time

inp = '';
while inp != 'q':
    inp = input(message)
    if inp == 'A':
        print("Status of all packages at a time between 8:35 a.m. and 9:25 a.m") #8:35 = 515
        print("Truck Print Time: " + minutesToTime(Truck1.printtime))
        print(Truck1.printpackages)
    elif inp == 'B':
        print("Status of all packages at a time between 9:35 a.m. and 10:25 a.m.") #9:35 = 575
        print("Truck Print Time: " + minutesToTime(Truck2.printtime))
        print(Truck2.printpackages)
    elif inp == 'C':
        print("Status of all packages at a time between 12:03 p.m. and 1:12 p.m.") #12:03 = 723
        print("Truck Print Time: " + minutesToTime(Truck3.printtime))
        print(Truck3.printpackages)
    elif inp == 'H':
        print("Truck 1 distance " + str(distance1))
        print("Truck 2 distance " + str(distance2))
        print("Truck 3 distance " + str(distance3))
        print("Total distance in miles " + str(distance1 + distance2 + distance3))
    elif inp.isdigit():
        try:
            val = int(inp)
            if val < 41:
                package = hashtable.get(val)
                print("########### PACKAGE INFO FOR PACKAGE " + inp + " ###########")
                print("########### [TIME IN MINS, STATUS]     ###########")
                print(package.history)
                package.print()
        except ValueError:
            print("No number found")
    elif inp != 'q':
        print("Please Enter A Valid Command")
