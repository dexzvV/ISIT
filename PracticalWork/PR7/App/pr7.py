import tkinter as tk
from tkinter import simpledialog, messagebox


class Node:
    def __init__(self, id, x, y, name):
        self.id = id
        self.x = x
        self.y = y
        self.name = name


class Edge:
    def __init__(self, start_node, end_node, capacity):
        self.start_node = start_node
        self.end_node = end_node
        self.capacity = capacity


class LogisticApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Логистическая сеть")
        self.nodes = []
        self.edges = []
        self.selected_node = None
        self.dragged_node = None
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.add_or_select_node)
        self.canvas.bind("<B1-Motion>", self.drag_node)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Button-3>", self.connect_nodes)
        tk.Button(root, text="Очистить", command=self.clear_all).pack()

    def add_or_select_node(self, event):
        for node in self.nodes:
            if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 < 400:
                self.selected_node = node
                self.dragged_node = node
                self.draw()
                return
        name = simpledialog.askstring("Ввод", "Название объекта:")
        if name:
            self.nodes.append(Node(len(self.nodes), event.x, event.y, name))
            self.draw()

    def drag_node(self, event):
        if self.dragged_node:
            self.dragged_node.x, self.dragged_node.y = event.x, event.y
            self.draw()

    def stop_drag(self, event):
        self.dragged_node = None

    def connect_nodes(self, event):
        target = next(
            (
                n
                for n in self.nodes
                if (event.x - n.x) ** 2 + (event.y - n.y) ** 2 < 400
            ),
            None,
        )
        if self.selected_node and target and self.selected_node != target:
            cap = simpledialog.askinteger("Ввод", "Пропускная способность:")
            if cap is not None:
                self.edges.append(Edge(self.selected_node, target, cap))
                self.draw()

    def clear_all(self):
        self.nodes, self.edges = [], []
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for e in self.edges:
            self.canvas.create_line(
                e.start_node.x, e.start_node.y, e.end_node.x, e.end_node.y
            )
            self.canvas.create_text(
                (e.start_node.x + e.end_node.x) / 2,
                (e.start_node.y + e.end_node.y) / 2,
                text=str(e.capacity),
            )
        for n in self.nodes:
            c = "orange" if n == self.selected_node else "lightblue"
            self.canvas.create_oval(n.x - 15, n.y - 15, n.x + 15, n.y + 15, fill=c)
            self.canvas.create_text(n.x, n.y + 25, text=n.name)


if __name__ == "__main__":
    LogisticApp(tk.Tk()).root.mainloop()
