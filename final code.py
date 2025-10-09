import heapq
import tkinter as tk
from tkinter import messagebox

class Graph:
    def __init__(self):
        self.graph = {}
        self.h_values = {}
        self.visual_nodes = {}

    def add_edge(self, node, neighbor, cost):
        if node not in self.graph:
            self.graph[node] = []
        self.graph[node].append((neighbor, cost))

    def set_heuristics(self, heuristics):
        self.h_values = heuristics

    def a_star_search(self, canvas, start, goal):
        pq = []
        heapq.heappush(pq, (self.h_values[start], start, [start], 0))
        visited = set()
        canvas.update()

        while pq:
            f_cost, current_node, path, g_cost = heapq.heappop(pq)
            canvas.itemconfig(self.visual_nodes[current_node]["oval"], fill="yellow")
            canvas.update()
            canvas.after(500)

            if current_node in visited:
                canvas.itemconfig(self.visual_nodes[current_node]["oval"], fill="grey")
                continue

            visited.add(current_node)

            if current_node == goal:
                for node in path:
                    canvas.itemconfig(self.visual_nodes[node]["oval"], fill="green")
                messagebox.showinfo("A* Search Result", f"Algorithm: A*\nPath found: {' -> '.join(path)}\nTotal Cost: {g_cost}")
                return path, g_cost

            for neighbor, cost in self.graph.get(current_node, []):
                if neighbor not in visited:
                    new_g_cost = g_cost + cost
                    new_f_cost = new_g_cost + self.h_values[neighbor]
                    heapq.heappush(pq, (new_f_cost, neighbor, path + [neighbor], new_g_cost))

            canvas.itemconfig(self.visual_nodes[current_node]["oval"], fill="grey")

        messagebox.showwarning("A* Search Result", "No path found.")
        return None, float('inf')

def visualize_graph(canvas, graph, edges):
    positions = {
        "A": (50, 50),
        "B": (150, 50),
        "C": (250, 50),
        "D": (150, 150),
        "E": (250, 150),
        "F": (150, 250)
    }

    canvas.delete("all")
    for node, (x, y) in positions.items():
        oval = canvas.create_oval(x, y, x+40, y+40, fill="white", outline="black")
        text = canvas.create_text(x+20, y+20, text=node)
        graph.visual_nodes[node] = {"oval": oval, "text": text}

    for edge, color in edges.items():
        x1, y1 = positions[edge[0]]
        x2, y2 = positions[edge[1]]
        canvas.create_line(x1+20, y1+20, x2+20, y2+20, fill=color, width=2)

def load_graph(graph, graph_data):
    graph.graph.clear()
    graph.visual_nodes.clear()
    for edge in graph_data["edges"]:
        graph.add_edge(*edge)
    graph.set_heuristics(graph_data["heuristics"])

def main():
    graph = Graph()
    graph_data_list = [
        {
            "edges": [("A", "B", 2), ("B", "C", 3), ("C", "D", 1)],
            "heuristics": {"A": 7, "B": 4, "C": 2, "D": 0},
            "edges_color": {("A", "B"): "blue", ("B", "C"): "green", ("C", "D"): "red"}
        },
        {
            "edges": [("A", "B", 1), ("B", "D", 4), ("A", "C", 2)],
            "heuristics": {"A": 6, "B": 5, "C": 4, "D": 0},
            "edges_color": {("A", "B"): "purple", ("B", "D"): "orange", ("A", "C"): "cyan"}
        },
        {
            "edges": [("A", "B", 3), ("B", "E", 2), ("E", "D", 1)],
            "heuristics": {"A": 8, "B": 5, "E": 3, "D": 0},
            "edges_color": {("A", "B"): "pink", ("B", "E"): "yellow", ("E", "D"): "black"}
        },
        {
            "edges": [("A", "C", 4), ("C", "D", 2), ("D", "F", 3)],
            "heuristics": {"A": 10, "C": 6, "D": 3, "F": 0},
            "edges_color": {("A", "C"): "red", ("C", "D"): "blue", ("D", "F"): "green"}
        },
        {
            "edges": [("A", "B", 2), ("B", "D", 3), ("D", "F", 1), ("A", "C", 2)],
            "heuristics": {"A": 7, "B": 4, "C": 6, "D": 2, "F": 0},
            "edges_color": {("A", "B"): "orange", ("B", "D"): "purple", ("D", "F"): "black", ("A", "C"): "cyan"}
        }
    ]

    root = tk.Tk()
    root.title("A* Search Visualization")

    canvas = tk.Canvas(root, width=400, height=300, bg="white")
    canvas.pack()

    graph_id = [0]  # Use a list to store graph_id

    def start_search():
        graph.a_star_search(canvas, "A", "D")

    def next_graph():
        if graph_id[0] < len(graph_data_list):
            graph_data = graph_data_list[graph_id[0]]
            load_graph(graph, graph_data)
            visualize_graph(canvas, graph, graph_data["edges_color"])
            graph_id[0] += 1
        else:
            messagebox.showinfo("End", "No more graphs to display.")
            graph_id[0] -= 1

    start_button = tk.Button(root, text="Start A* Search", command=start_search)
    start_button.pack()

    next_button = tk.Button(root, text="Next Graph", command=next_graph)
    next_button.pack()

    next_graph()  # Load the first graph
    root.mainloop()

if __name__ == "__main__":
    main()
