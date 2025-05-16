#include <iostream>
#include <map>
#include <queue>
#include <climits>
#include <vector>
using namespace std;

// QuickSort Partition Function
int partition(vector<int>& locations, int start, int end) {
    int pivot = locations[end];
    int i = start - 1;
    for (int j = start; j < end; j++) {
        if (locations[j] <= pivot) {
            i++;
            int temp = locations[i];
            locations[i] = locations[j];
            locations[j] = temp;
        }
    }
    int temp = locations[i+1];
    locations[i+1] = locations[end];
    locations[end] = temp;
    return i + 1;
}

// QuickSort Function
void quickSortDeliveryLocations(vector<int>& locations, int start, int end) {
    if (start < end) {
        int pivotIndex = partition(locations, start, end);
        quickSortDeliveryLocations(locations, start, pivotIndex - 1);
        quickSortDeliveryLocations(locations, pivotIndex + 1, end);
    }
}

// Dijkstra's Algorithm with Path Tracking
void dijkstraShortestRoutes(
    map<int, map<int, int> >& graph,
    int startNode,
    map<int, int>& distances,
    map<int, int>& previous
) {
    map<int, bool> visited;

    // Initialize distances
    for (map<int, map<int, int> >::iterator it = graph.begin(); it != graph.end(); ++it) {
        distances[it->first] = INT_MAX;
        visited[it->first] = false;
        previous[it->first] = -1;
    }

    distances[startNode] = 0;

    for (size_t i = 0; i < graph.size(); i++) {
        int minDistance = INT_MAX;
        int minVertex = -1;

        // Find unvisited vertex with the smallest distance
        for (map<int, map<int, int> >::iterator it = graph.begin(); it != graph.end(); ++it) {
            if (!visited[it->first] && distances[it->first] < minDistance) {
                minDistance = distances[it->first];
                minVertex = it->first;
            }
        }

        if (minVertex == -1) break;

        visited[minVertex] = true;

        // Update neighbors
        for (map<int, int>::iterator neighborIt = graph[minVertex].begin(); 
             neighborIt != graph[minVertex].end(); ++neighborIt) {
            int neighborNode = neighborIt->first;
            int weight = neighborIt->second;

            if (!visited[neighborNode] && distances[minVertex] + weight < distances[neighborNode]) {
                distances[neighborNode] = distances[minVertex] + weight;
                previous[neighborNode] = minVertex;
            }
        }
    }
}

// Print the path from start to a node using the previous map
void printPath(int node, map<int, int>& previous) {
    if (previous[node] == -1) {
        cout << node;
        return;
    }
    printPath(previous[node], previous);
    cout << " -> " << node;
}

int main() {
    int numIntersections;
    cout << "Enter the number of intersections: ";
    cin >> numIntersections;

    if (numIntersections <= 0) {
        cerr << "Error: Number of intersections must be positive." << endl;
        return 1;
    }

    vector<int> deliveryLocations(numIntersections);
    for (int i = 0; i < numIntersections; i++) {
        deliveryLocations[i] = i;
    }

    map<int, map<int, int> > roadNetworkGraph;

    for (int i = 0; i < numIntersections; i++) {
        int numNeighbours;
        cout << "Enter the number of neighbors for intersection " << i << ": ";
        cin >> numNeighbours;

        if (numNeighbours < 0 || numNeighbours >= numIntersections) {
            cerr << "Error: Invalid number of neighbors." << endl;
            return 1;
        }

        for (int j = 0; j < numNeighbours; j++) {
            int neighbor, distance;
            cout << "  Enter neighbor ID for intersection " << i << ": ";
            cin >> neighbor;
            
            if (neighbor < 0 || neighbor >= numIntersections) {
                cerr << "Error: Invalid neighbor ID." << endl;
                return 1;
            }

            cout << "  Enter distance to neighbor " << neighbor << ": ";
            cin >> distance;
            
            if (distance <= 0) {
                cerr << "Error: Distance must be positive." << endl;
                return 1;
            }

            // Add both directions for undirected graph
            roadNetworkGraph[i][neighbor] = distance;
            roadNetworkGraph[neighbor][i] = distance;
        }
    }

    // Sort delivery locations
    quickSortDeliveryLocations(deliveryLocations, 0, numIntersections - 1);

    // Compute shortest routes from startNode (0)
    map<int, int> distances;
    map<int, int> previous;
    dijkstraShortestRoutes(roadNetworkGraph, 0, distances, previous);

    // Output with path tracing
    cout << "\nOptimized Delivery Routes from Intersection 0:\n";
    for (vector<int>::iterator it = deliveryLocations.begin(); it != deliveryLocations.end(); ++it) {
        int destination = *it;
        cout << "To Intersection " << destination << " -> Distance: ";

        if (distances.find(destination) == distances.end() || distances[destination] == INT_MAX) {
            cout << "Unreachable";
        } else {
            cout << distances[destination] << " -> Path: ";
            printPath(destination, previous);
        }
        cout << endl;
    }

    return 0;
}