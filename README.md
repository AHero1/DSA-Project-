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

<img width="488" alt="Screenshot 2025-05-17 at 2 44 41 AM" src="https://github.com/user-attachments/assets/a1a386fd-e964-49be-8aa4-4e819750638c" />

# GUI

<img width="1184" alt="Screenshot 2025-05-17 at 9 02 48 AM" src="https://github.com/user-attachments/assets/3f9d5224-bbb6-4fa1-9bfd-f102146aa900" />

## Using OpenStreetMap (OSM) Data

To generate realistic road maps, we use OpenStreetMap (OSM) `.osm` files.

### Step 1: Export OSM Map
We selected and downloaded a small area (e.g., campus, neighborhood).
<img width="1361" alt="Screenshot 2025-05-17 at 9 11 54 AM" src="https://github.com/user-attachments/assets/de94a332-6979-434c-a6b8-6a95350aef97" />

- Zoom into the region
- Export
- Save the file as `map.osm`

### Step 2: Parsing OSM File

The `loadOSM()` function in our `Graph` class:
- Parses OSM XML to extract `<node>` and `<way>` elements.
- Builds a graph:
  - Nodes = Road intersections (with lat/lon)
  - Edges = Roads between them (weighted by distance)

### Step 3: Coordinate Mapping

To visualize or calculate distances, the latitude/longitude of nodes are converted into:
- Cartesian coordinates (x, y) for GUI
- Real-world distance (e.g., using Haversine formula)
- The Haversine formula is used to calculate the great-circle distance between two points on a sphere, given their longitudes and latitudes. It essentially finds the shortest distance between two points on the surface of a sphere, like the Earth, ignoring any terrain variations. 

# GUI with Map Integration 
![WhatsApp Image 2025-05-17 at 01 19 45](https://github.com/user-attachments/assets/7db9c6c6-6983-4ce5-a516-612724f9da47)

