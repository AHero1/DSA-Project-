# Delivery Route Optimization System
## Objective
The goal of this project is to develop an efficent package delivery system that minimizes travel time and optimizes delivery routes. By leveraging Quicksort to arrange delivery locations in an optimal order and Dijkstra’s Algorithmto compute the shortest paths, the system will ensure faster and more cost-eEective deliveries. This approach will help improve logistics eEiciency, reduce fuel consumption, and enhance overall delivery performance.
## Algorithms Used:
This project uses QuickSort and Dijkstra's Algorithm to optimize delivery routes in a city modeled as a graph of intersections.
## QuickSort – For Sorting Delivery Locations
QuickSort is used to sort the delivery locations (intersections) before computing the shortest paths. Sorting ensures that output is predictable and organized.
### How QuickSort works:
Uses divide and conquer by choosing a pivot.
Partitions the array so values less than the pivot are left, and greater are right.
Recursively sorts left and right sub-arrays.
### Time Complexity: 
Best & Average: O(n log n), Worst: O(n^2) (rare with good pivot choices)
## Dijkstra’s Algorithm – For Shortest Routes
Dijkstra's algorithm finds the shortest paths from the starting intersection (0) to all others.

### How it works:
-Starts at a source node and assigns it a distance of 0.

-All other nodes start with infinite distance.

-Repeatedly selects the closest unvisited node and updates the distances to its neighbors.

-Builds the shortest path tree using a previous map to track route history.
### Output:
Distance from source
Actual path taken (like 0 -> 2 -> 4 -> 5)
### Time Complexity: O(V^2) with maps
(Use priority queue + min-heap for faster O(E + log V) in advanced versions)
min-heap for faster O(E + log V) in advanced versions)

![Uploading Screenshot 2025-05-17 at 2.44.41 AM.png…]()
