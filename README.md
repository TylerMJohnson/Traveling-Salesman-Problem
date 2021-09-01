# WGUC950

The purpose of this project is to determine the best route and delivery distribution for the Western Governors University Parcel Service (WGUPS) using a common high-level programming language (Python 3.7). There are 40 packages that must be split up across two trucks with 3 different drivers. Some packages have delivery constraints, and some have been delayed. Additionally, there is a package that initially has the wrong address and packages that must go out on the second truck. To solve this problem, we must first use a series of conditional statements to load the trucks based on the data that is provided. We then must implement a greedy algorithm to optimize delivery of each package along the truck route. This algorithm is greedy because it determines the shortest available path from its current location then continues to do this until no additional packages remain. This article will analyze the use of this algorithm and provide a descriptive overview of the applications methods and components. 

Algorithm Overview: 

The greedy algorithm is executed by doing the following… 

A list of packages on the truck is passed in along with the associated truck number and the current location (always at hub by default) 

The current location is compared to the locations of all the packages in the truck to determine the closest location. 

The lowest value is determined once all objects in the truck have been compared then that value is removed from the truck list and the truck moves to that address location 

That value is appended to an optimized location list than the algorithm updates current location with the new address and calls the function again with the smaller truck list. 

 

The space-time complexity of this self-adjusting greedy algorithm has a worst case runtime O(N^2) and a best case runtime of O(1). The worst case is almost always guaranteed as the best case is only possible when the list of packages being loaded onto a truck is empty. 
