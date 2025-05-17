import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import math
import heapq
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk

# QuickSort with Random Pivot
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

# Dijkstra's Algorithm
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

# Get path as string
def getPath(node, previous):
    if previous[node] == -1:
        return str(node)
    return getPath(previous[node], previous) + " -> " + str(node)

# Haversine formula to calculate distance between two lat/lon points (in km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Tkinter GUI with OSM Integration
class DeliverySystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Route Optimization with OSM")
        self.root.geometry("1200x800")
        
        self.graph = {}
        self.node_positions = []
        self.distances = {}
        self.previous = {}
        self.num_intersections = 0
        self.current_node = 0
        self.scale_factor = 1.0
        self.node_coords = {}  # Store lat/lon for OSM nodes
        self.map_image = None  # Store the map background image
        self.map_photo = None  # Store the PhotoImage for the canvas
        self.canvas_width = 800  # Default canvas width
        self.canvas_height = 700  # Default canvas height
        
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
        
        # Buttons
        self.compute_button = ttk.Button(self.input_frame, text="Compute Routes", command=self.compute_routes)
        ttk.Button(self.input_frame, text="Load OSM File", command=self.load_osm_file).grid(row=2, column=0, columnspan=3, pady=5)
        ttk.Button(self.input_frame, text="Export Graph", command=self.export_graph).grid(row=3, column=0, columnspan=3, pady=5)
        ttk.Button(self.input_frame, text="Zoom In", command=self.zoom_in).grid(row=4, column=0, pady=5)
        ttk.Button(self.input_frame, text="Zoom Out", command=self.zoom_out).grid(row=4, column=1, pady=5)
        ttk.Button(self.input_frame, text="Reset", command=self.reset).grid(row=4, column=2, pady=5)
        
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
        
        self.canvas_frame = ttk.Frame(self.graph_frame)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas = tk.Canvas(self.canvas_frame, width=799, height=702, bg="white")  # Match initial image size
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
    
    def load_osm_file(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("OSM files", "*.osm")], initialdir="/Users/ahero1/Projects/DeliveryRoute")
            if not filename:
                return
            tree = ET.parse(filename)
            root = tree.getroot()
            
            # Configurable parameters
            max_nodes = 50  # Maximum number of nodes to load
            min_lat, max_lat = 33.641547, 33.643007  # Islamabad bounding box
            min_lon, max_lon = 72.990970, 72.993065  # Islamabad bounding box
            
            # Extract nodes (intersections) with a maximum limit and bounding box
            nodes = {}
            node_count = 0
            for node in root.findall("node"):
                if node_count >= max_nodes:
                    break
                lat = float(node.get("lat", 0))
                lon = float(node.get("lon", 0))
                # Debugging: Print first few nodes to verify coordinates
                if node_count < 5:
                    print(f"Node {node.get('id')}: lat={lat}, lon={lon}")
                if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                    node_id = int(node.get("id", -1))
                    if node_id != -1:
                        nodes[node_id] = (lat, lon)
                        node_count += 1
            
            if not nodes:
                messagebox.showwarning("Warning", f"No nodes found within lat {min_lat} to {max_lat}, lon {min_lon} to {max_lon} or limit of {max_nodes}. Check file or adjust bounding box.")
                return
            
            # Map node IDs to sequential integers starting from 0
            node_mapping = {old_id: new_id for new_id, old_id in enumerate(nodes.keys())}
            self.node_coords = {new_id: nodes[old_id] for old_id, new_id in node_mapping.items()}
            self.num_intersections = len(self.node_coords)
            
            # Initialize graph
            self.graph = {i: {} for i in range(self.num_intersections)}
            
            # Extract ways (roads/edges) for the filtered nodes
            for way in root.findall("way"):
                tags = way.findall("tag")
                is_highway = any(tag.get("k") == "highway" for tag in tags)
                if not is_highway:
                    continue
                nds = [int(nd.get("ref")) for nd in way.findall("nd") if int(nd.get("ref")) in nodes]
                if len(nds) < 2:  # Skip if not enough valid nodes
                    continue
                for i in range(len(nds) - 1):
                    u = node_mapping.get(nds[i])
                    v = node_mapping.get(nds[i + 1])
                    if u is not None and v is not None:
                        lat1, lon1 = self.node_coords[u]
                        lat2, lon2 = self.node_coords[v]
                        distance = haversine(lat1, lon1, lat2, lon2)
                        self.graph[u][v] = distance
                        self.graph[v][u] = distance
            
            # Load map background image and set canvas size dynamically
            self.map_image = Image.open("/Users/ahero1/Downloads/map-3.png")
            self.canvas_width, self.canvas_height = self.map_image.size  # Get actual image size
            self.canvas.config(width=self.canvas_width, height=self.canvas_height)
            self.map_photo = ImageTk.PhotoImage(self.map_image)
            self.canvas.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.map_photo)  # Center the image
            
            # Position nodes on canvas using lat/lon
            self.position_osm_nodes()
            
            # Update UI
            self.intersections_entry.delete(0, tk.END)
            self.intersections_entry.insert(0, str(self.num_intersections))
            self.intersections_entry.config(state="disabled")
            self.edge_frame.grid_remove()
            self.compute_button.grid(row=1, column=0, columnspan=3, pady=5)
            self.current_node = self.num_intersections  # Skip manual edge input
            messagebox.showinfo("Success", f"Loaded OSM file with {self.num_intersections} intersections.")
        except ET.ParseError as e:
            messagebox.showerror("Error", f"Invalid OSM file format: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load OSM file: {e}")
    
    def position_osm_nodes(self):
        if not self.node_coords:
            return
        
        # Find min/max lat/lon for scaling
        lats = [coords[0] for coords in self.node_coords.values()]
        lons = [coords[1] for coords in self.node_coords.values()]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)
        
        # Avoid division by zero
        lat_range = max_lat - min_lat if max_lat != min_lat else 1
        lon_range = max_lon - min_lon if max_lon != min_lon else 1
        
        # Scale lat/lon to canvas coordinates (center dynamically based on image size)
        self.node_positions = []
        for i in range(self.num_intersections):
            lat, lon = self.node_coords[i]
            x = (self.canvas_width / 2) + (lon - min_lon) / lon_range * (self.canvas_width - 200) - (self.canvas_width - 200) / 2
            y = (self.canvas_height / 2) - (lat - min_lat) / lat_range * (self.canvas_height - 200) + (self.canvas_height - 200) / 2
            self.node_positions.append((x, y))
    
    def export_graph(self):
        try:
            with open("graph_export.txt", "w") as f:
                f.write(f"Number of Intersections: {self.num_intersections}\n")
                f.write("Edges:\n")
                for u in self.graph:
                    for v, w in self.graph[u].items():
                        if u < v:  # Avoid duplicates
                            f.write(f"{u} {v} {w:.2f}\n")
            messagebox.showinfo("Success", "Graph exported to graph_export.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export graph: {e}")
    
    def zoom_in(self):
        self.scale_factor *= 1.2
        self.compute_routes()
    
    def zoom_out(self):
        self.scale_factor /= 1.2
        if self.scale_factor < 0.5:
            self.scale_factor = 0.5
        self.compute_routes()
    
    def start_input(self):
        try:
            self.num_intersections = int(self.intersections_entry.get())
            if self.num_intersections <= 0:
                messagebox.showerror("Error", "Number of intersections must be positive.")
                return
            self.graph = {i: {} for i in range(self.num_intersections)}
            self.node_positions = []
            radius = min(200, 600 / (self.num_intersections + 1))
            center_x, center_y = 400, 400
            for i in range(self.num_intersections):
                angle = 2 * math.pi * i / self.num_intersections
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.node_positions.append((x, y))
            self.current_node = 0
            self.node_coords = {}  # Clear OSM coords if using manual input
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
            dist_text = str(round(dist, 2)) if dist != float('inf') else "Unreachable"
            self.results_table.insert("", tk.END, values=(node, dist_text, path))
            if dist != float('inf'):
                reachable += 1
                total_distance += dist
        
        # Update Summary
        summary = (
            f"Total Reachable Intersections: {reachable}/{self.num_intersections}\n"
            f"Total Distance: {round(total_distance, 2)}\n"
            f"Average Distance: {round(total_distance / reachable, 2) if reachable > 0 else 0:.2f}\n"
            f"Estimated Fuel Cost: ${round(total_distance * 0.1, 2):.2f}"
        )
        self.summary_label.config(text=summary)
        
        # Draw Graph
        self.canvas.delete("all")
        if self.map_image:
            self.canvas.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.map_photo)  # Redraw background
        
        self.canvas.configure(scrollregion=(0, 0, self.canvas_width + 100, self.canvas_height + 100))
        
        # Draw edges
        for u in self.graph:
            for v, w in self.graph[u].items():
                if u < v:
                    x1, y1 = self.node_positions[u]
                    x2, y2 = self.node_positions[v]
                    x1_scaled = x1 * self.scale_factor
                    y1_scaled = y1 * self.scale_factor
                    x2_scaled = x2 * self.scale_factor
                    y2_scaled = y2 * self.scale_factor
                    color = f"#{min(int(w * 20) % 255, 255):02x}00{max(255 - int(w * 20) % 255, 0):02x}"
                    self.canvas.create_line(x1_scaled, y1_scaled, x2_scaled, y2_scaled, fill=color, width=2)
                    self.canvas.create_text((x1_scaled + x2_scaled) / 2, (y1_scaled + y2_scaled) / 2, text=f"{w:.1f}", fill="black")
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
        node_radius = 15 * self.scale_factor
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
        self.node_coords = {}
        self.map_image = None
        self.map_photo = None
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
        self.canvas.config(width=799, height=702)  # Reset to initial size
        self.canvas.configure(scrollregion=(0, 0, 799 + 100, 702 + 100))

if __name__ == "__main__":
    root = tk.Tk()
    app = DeliverySystemGUI(root)
    root.mainloop()