import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import heapq

# QuickSort with Random Pivot (from your C++ code)
def partition(locations, start, end):
    pivot_idx = random.randint(start, end)
    locations[pivot_idx], locations[end] = locations[end], locations[pivot_idx]
    pivot = locations[end][1]  # Sort by distance
    i = start - 1
    for j in range(start, end):
        if locations[j][1] <= pivot:
            i += 1
            locations[i], locations[j] = locations[j], locations[i]
    locations[i + 1], locations[end] = locations[end], locations[i + 1]
    return i + 1

def quickSortDeliveryLocations(locations, start, end):
    if start < end:
        pivot_index = partition(locations, start, end)
        quickSortDeliveryLocations(locations, start, pivot_index - 1)
        quickSortDeliveryLocations(locations, pivot_index + 1, end)

# Dijkstra's Algorithm with Priority Queue (from your C++ code)
def dijkstraShortestRoutes(graph, start_node):
    distances = {node: float('inf') for node in graph}
    previous = {node: -1 for node in graph}
    distances[start_node] = 0
    pq = [(0, start_node)]
    
    while pq:
        dist, node = heapq.heappop(pq)
        if dist > distances[node]:
            continue
        for neighbor, weight in graph[node].items():
            new_dist = distances[node] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances, previous

# Get path as string (from your C++ code)
def getPath(node, previous):
    if previous[node] == -1:
        return str(node)
    return getPath(previous[node], previous) + " -> " + str(node)

# Tkinter GUI
class DeliverySystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Route Optimization")
        self.root.geometry("1200x800")
        
        self.graph = {}
        self.node_positions = []
        self.distances = {}
        self.previous = {}
        self.num_intersections = 0
        self.current_node = 0
        self.scale_factor = 1.0  # For zooming
        
        # Input Frame
        self.input_frame = ttk.LabelFrame(root, text="Input", padding=10)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        
        # Intersections Input
        ttk.Label(self.input_frame, text="Number of Intersections:").grid(row=0, column=0, sticky="w")
        self.intersections_entry = ttk.Entry(self.input_frame, width=10)
        self.intersections_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.input_frame, text="Start", command=self.start_input).grid(row=0, column=2, padx=5, pady=5)
        
        # Edge Input
        self.edge_frame = ttk.LabelFrame(self.input_frame, text="Add Edge", padding=10)
        ttk.Label(self.edge_frame, text="Neighbor ID:").grid(row=0, column=0, sticky="w")
        self.neighbor_entry = ttk.Entry(self.edge_frame, width=10)
        self.neighbor_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.edge_frame, text="Distance:").grid(row=1, column=0, sticky="w")
        self.distance_entry = ttk.Entry(self.edge_frame, width=10)
        self.distance_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.edge_frame, text="Add Edge", command=self.add_edge).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(self.edge_frame, text="Next Intersection", command=self.next_intersection).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Compute, Zoom, and Reset Buttons
        self.compute_button = ttk.Button(self.input_frame, text="Compute Routes", command=self.compute_routes)
        ttk.Button(self.input_frame, text="Zoom In", command=self.zoom_in).grid(row=3, column=0, pady=5)
        ttk.Button(self.input_frame, text="Zoom Out", command=self.zoom_out).grid(row=3, column=1, pady=5)
        ttk.Button(self.input_frame, text="Reset", command=self.reset).grid(row=3, column=2, pady=5)
        
        # Results Frame
        self.results_frame = ttk.LabelFrame(root, text="Results", padding=10)
        self.results_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.results_table = ttk.Treeview(self.results_frame, columns=("Intersection", "Distance", "Path"), show="headings")
        self.results_table.heading("Intersection", text="Intersection")
        self.results_table.heading("Distance", text="Distance")
        self.results_table.heading("Path", text="Path")
        self.results_table.column("Intersection", width=100)
        self.results_table.column("Distance", width=100)
        self.results_table.column("Path", width=300)
        self.results_table.grid(row=0, column=0, sticky="nsew")
        
        self.summary_label = ttk.Label(self.results_frame, text="")
        self.summary_label.grid(row=1, column=0, pady=10)
        
        # Graph Canvas with Scrollbars
        self.graph_frame = ttk.LabelFrame(root, text="Graph Visualization", padding=10)
        self.graph_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Canvas inside a Frame with Scrollbars
        self.canvas_frame = ttk.Frame(self.graph_frame)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas = tk.Canvas(self.canvas_frame, width=700, height=700, bg="white")
        self.scroll_x = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.graph_frame.columnconfigure(0, weight=1)
        self.graph_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)
        
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
    
    def zoom_in(self):
        self.scale_factor *= 1.2
        self.compute_routes()  # Redraw with new scale
    
    def zoom_out(self):
        self.scale_factor /= 1.2
        if self.scale_factor < 0.5:
            self.scale_factor = 0.5
        self.compute_routes()  # Redraw with new scale
    
    def start_input(self):
        try:
            self.num_intersections = int(self.intersections_entry.get())
            if self.num_intersections <= 0:
                messagebox.showerror("Error", "Number of intersections must be positive.")
                return
            self.graph = {i: {} for i in range(self.num_intersections)}
            self.node_positions = []
            # Adjust radius based on number of nodes to prevent overlap
            radius = min(200, 600 / (self.num_intersections + 1))  # Dynamic radius
            center_x, center_y = 400, 400  # Adjusted center for larger scrollregion
            for i in range(self.num_intersections):
                angle = 2 * math.pi * i / self.num_intersections
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.node_positions.append((x, y))
            self.current_node = 0
            self.edge_frame.grid(row=1, column=0, columnspan=3, pady=10)
            self.compute_button.grid(row=2, column=0, columnspan=3, pady=5)
            self.intersections_entry.config(state="disabled")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
    
    def add_edge(self):
        try:
            neighbor = int(self.neighbor_entry.get())
            distance = int(self.distance_entry.get())
            if neighbor < 0 or neighbor >= self.num_intersections or neighbor == self.current_node:
                messagebox.showerror("Error", "Invalid neighbor ID.")
                return
            if distance <= 0:
                messagebox.showerror("Error", "Distance must be positive.")
                return
            self.graph[self.current_node][neighbor] = distance
            self.graph[neighbor][self.current_node] = distance
            self.neighbor_entry.delete(0, tk.END)
            self.distance_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
    
    def next_intersection(self):
        self.current_node += 1
        if self.current_node >= self.num_intersections:
            self.edge_frame.grid_remove()
        else:
            self.edge_frame.config(text=f"Add Edge for Intersection {self.current_node}")
    
    def compute_routes(self):
        if self.current_node < self.num_intersections:
            messagebox.showerror("Error", "Please complete edge input for all intersections.")
            return
        self.distances, self.previous = dijkstraShortestRoutes(self.graph, 0)
        sorted_locations = [(i, self.distances[i]) for i in range(self.num_intersections)]
        quickSortDeliveryLocations(sorted_locations, 0, len(sorted_locations) - 1)
        
        # Update Results Table
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        reachable = 0
        total_distance = 0
        for node, dist in sorted_locations:
            path = getPath(node, self.previous) if dist != float('inf') else "-"
            dist_text = str(dist) if dist != float('inf') else "Unreachable"
            self.results_table.insert("", tk.END, values=(node, dist_text, path))
            if dist != float('inf'):
                reachable += 1
                total_distance += dist
        
        # Update Summary
        summary = (
            f"Total Reachable Intersections: {reachable}/{self.num_intersections}\n"
            f"Total Distance: {total_distance}\n"
            f"Average Distance: {total_distance / reachable if reachable > 0 else 0:.2f}\n"
            f"Estimated Fuel Cost: ${total_distance * 0.1:.2f}"
        )
        self.summary_label.config(text=summary)
        
        # Draw Graph with Scaling
        self.canvas.delete("all")
        # Set scrollregion to accommodate larger graphs
        self.canvas.configure(scrollregion=(0, 0, 900, 900))  # Larger virtual canvas
        
        # Draw edges
        for u in self.graph:
            for v, w in self.graph[u].items():
                if u < v:
                    x1, y1 = self.node_positions[u]
                    x2, y2 = self.node_positions[v]
                    # Apply scaling
                    x1_scaled = x1 * self.scale_factor
                    y1_scaled = y1 * self.scale_factor
                    x2_scaled = x2 * self.scale_factor
                    y2_scaled = y2 * self.scale_factor
                    color = f"#{w * 20 % 255:02x}00{255 - w * 20 % 255:02x}"
                    self.canvas.create_line(x1_scaled, y1_scaled, x2_scaled, y2_scaled, fill=color, width=2)
                    self.canvas.create_text((x1_scaled + x2_scaled) / 2, (y1_scaled + y2_scaled) / 2, text=str(w), fill="black")
        # Draw shortest paths
        for i in range(1, self.num_intersections):
            if self.distances[i] != float('inf'):
                path = []
                at = i
                while at != -1:
                    path.append(at)
                    at = self.previous[at]
                path.reverse()
                for j in range(1, len(path)):
                    u, v = path[j - 1], path[j]
                    x1, y1 = self.node_positions[u]
                    x2, y2 = self.node_positions[v]
                    x1_scaled = x1 * self.scale_factor
                    y1_scaled = y1 * self.scale_factor
                    x2_scaled = x2 * self.scale_factor
                    y2_scaled = y2 * self.scale_factor
                    self.canvas.create_line(x1_scaled, y1_scaled, x2_scaled, y2_scaled, fill="red", width=3)
        # Draw nodes
        node_radius = 15 * self.scale_factor  # Scale node size
        for i in range(self.num_intersections):
            x, y = self.node_positions[i]
            x_scaled = x * self.scale_factor
            y_scaled = y * self.scale_factor
            fill = "red" if i == 0 else "blue"
            self.canvas.create_oval(x_scaled - node_radius, y_scaled - node_radius, x_scaled + node_radius, y_scaled + node_radius, fill=fill)
            self.canvas.create_text(x_scaled + 30 * self.scale_factor, y_scaled, text=str(i), fill="black")
    
    def reset(self):
        self.graph = {}
        self.node_positions = []
        self.distances = {}
        self.previous = {}
        self.num_intersections = 0
        self.current_node = 0
        self.scale_factor = 1.0
        self.intersections_entry.config(state="normal")
        self.intersections_entry.delete(0, tk.END)
        self.neighbor_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.edge_frame.grid_remove()
        self.compute_button.grid_remove()
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        self.summary_label.config(text="")
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=(0, 0, 700, 700))

if __name__ == "__main__":
    root = tk.Tk()
    app = DeliverySystemGUI(root)
    root.mainloop()