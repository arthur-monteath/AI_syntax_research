import tkinter as tk
from grammar import generate_tree, linearize
from layout import layout_tree

WIDTH = 900
HEIGHT = 600
NODE_RADIUS = 18

class SyntaxGUI:
    def __init__(self, root):
        self.root = root
        root.title("Syntax Generator")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#111")
        self.canvas.pack(fill="both", expand=True)

        self.button = tk.Button(
            root,
            text="Generate sentence",
            command=self.generate,
            bg="#222",
            fg="#eee",
            relief="flat",
            padx=20,
            pady=8
        )
        self.button.pack(pady=10)

        self.generate()

    def generate(self):
        self.canvas.delete("all")

        tree = generate_tree("S")
        positions = layout_tree(tree, x=50, y=50, level_gap=50)

        for parent, (px, py) in positions.items():
            for child in parent.children:
                cx, cy = positions[child]
                self.canvas.create_line(px, py, cx, cy, fill="#666", width=1.5)

        for node, (x, y) in positions.items():
            self.canvas.create_oval(
                x - NODE_RADIUS, y - NODE_RADIUS,
                x + NODE_RADIUS, y + NODE_RADIUS,
                fill="#1e1e1e",
                outline="#aaa"
            )
            self.canvas.create_text(x, y, text=node.label, fill="#eee")

        sentence = linearize(tree).capitalize() + "."
        self.canvas.create_text(
            WIDTH // 2, HEIGHT - 30,
            text=sentence,
            fill="#bbb",
            font=("Helvetica", 14)
        )


if __name__ == "__main__":
    root = tk.Tk()
    SyntaxGUI(root)
    root.mainloop()