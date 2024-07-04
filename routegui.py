import time
import tkinter as tk
from tkinter import messagebox


class Node:
    def __init__(self, x, y, terrain_type=0):
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.g = 0
        self.h = 0
        self.f = 0
        self.connection = None
        self.neighbors = []

    def get_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def get_cost(self):
        costs = {0: 1, 1: float("inf"), 2: 3, 3: 2}  # Normal, Wall, Water, Construction # Por que en diccionario?
        return costs[self.terrain_type]


class PathfindingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("A* Pathfinding Visualization")

        self.cell_size = 50
        self.grid_size = 16

        self.canvas = tk.Canvas(
            self.master,
            width=self.cell_size * self.grid_size,
            height=self.cell_size * self.grid_size,
        )
        self.canvas.pack()

        self.mapa = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.start = None
        self.end = None

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.on_click)

        self.terrain_var = tk.StringVar(value="Wall")
        terrain_options = ["Wall", "Water", "Bache", "Normal"]
        terrain_menu = tk.OptionMenu(self.master, self.terrain_var, *terrain_options)
        terrain_menu.pack()

        find_path_button = tk.Button(
            self.master, text="Find Path", command=self.find_path
        )
        find_path_button.pack()

        reset_button = tk.Button(self.master, text="Reset", command=self.reset)
        reset_button.pack()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = i * self.cell_size
                y1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill_color = self.get_color(self.mapa[j][i])
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill_color, outline="black"
                )

        if self.start:
            self.draw_point(self.start[0], self.start[1], "green")
        if self.end:
            self.draw_point(self.end[0], self.end[1], "red")

    def get_color(self, terrain_type):
        colors = {0: "white", 1: "black", 2: "blue", 3: "orange"}
        return colors.get(terrain_type, "white")

    def draw_point(self, x, y, color):
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color)

    def on_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        if not self.start:
            self.start = (x, y)
        elif not self.end:
            self.end = (x, y)
        else:
            terrain_type = {"Wall": 1, "Water": 2, "Bache": 3, "Normal": 0}[
                self.terrain_var.get()
            ]
            self.mapa[y][x] = terrain_type

        self.draw_grid()

    def find_path(self):
        if not self.start or not self.end:
            messagebox.showwarning("Warning", "Please set both start and end points.")
            return

        nodes = self.create_nodes()
        start_node = nodes[self.start[1]][self.start[0]]
        end_node = nodes[self.end[1]][self.end[0]]
        path = self.a_star(start_node, end_node)

        if path:
            self.visualize_path(path)
            messagebox.showinfo("Success", "Path found!")
        else:
            messagebox.showinfo("No Path", "No path could be found.")

    def create_nodes(self):
        nodes = [
            [Node(x, y, self.mapa[y][x]) for x in range(self.grid_size)]
            for y in range(self.grid_size)
        ]
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if x > 0:
                    nodes[y][x].neighbors.append(nodes[y][x - 1])
                if x < self.grid_size - 1:
                    nodes[y][x].neighbors.append(nodes[y][x + 1])
                if y > 0:
                    nodes[y][x].neighbors.append(nodes[y - 1][x])
                if y < self.grid_size - 1:
                    nodes[y][x].neighbors.append(nodes[y + 1][x])
        return nodes

    def a_star(self, start_node, target_node):
        to_search = [start_node]
        processed = []

        while to_search:
            current = min(to_search, key=lambda x: (x.f, x.h))
            processed.append(current)
            to_search.remove(current)

            if current == target_node:
                path = []
                while current != start_node:
                    path.append(current)
                    current = current.connection
                path.append(start_node)
                return path[::-1]

            for neighbor in current.neighbors:
                if neighbor.terrain_type == 1 or neighbor in processed:
                    continue

                cost_to_neighbor = (
                    current.g + current.get_distance(neighbor) * neighbor.get_cost()
                )

                if neighbor not in to_search or cost_to_neighbor < neighbor.g:
                    neighbor.g = cost_to_neighbor
                    neighbor.connection = current
                    if neighbor not in to_search:
                        neighbor.h = neighbor.get_distance(target_node)
                        to_search.append(neighbor)

                neighbor.f = neighbor.g + neighbor.h

        return None

    def visualize_path(self, path):
        for node in path:
            if (node.x, node.y) != self.start and (node.x, node.y) != self.end:
                self.draw_point(node.x, node.y, "yellow")
                self.master.update()
                time.sleep(0.1)

    def reset(self):
        self.mapa = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.start = None
        self.end = None
        self.draw_grid()


if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingGUI(root)
    root.mainloop()
