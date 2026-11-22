import tkinter as tk
from circuit import Circuit

root = tk.Tk()
root.title("WireLab")
root.geometry("900x400")

# circuit.py imports
circuit = Circuit()
tool = "select"
start = None
colors = {"led": "red", "resistor": "tan", "button": "black"}
hole_pos = {}
hole_at = {}

# Breadboard Values
SPACING = 30
RADIUS = 9
START_X = 50
START_Y = 50
GAP = 20

# Breadboard Canvas
canvas = tk.Canvas(root, width=700, height=400, bg="#e8eee5")
canvas.grid(row=0, column=1)

panel = tk.Frame(root, padx=10, pady=10)
panel.grid(row=0, column=0, sticky="ns")

holes = {}

for col in range(20):
    for row in range(10):
        x = START_X + (SPACING * col)
        y = START_Y + (SPACING * row)
        if row >= 5:
            y += GAP

        hole = canvas.create_oval(
            x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="#bcc7bf", tags="hole"
        )
        holes[(col, row)] = hole
        hole_at[hole] = (col, row)
        hole_pos[(col, row)] = (x, y)

# -----------------

def pick_tool(name):
    global tool, start
    tool = name
    start = None

tk.Button(panel, text="LED", command=lambda: pick_tool("led")).pack(fill="x")
tk.Button(panel, text="Resistor", command=lambda: pick_tool("resistor")).pack(fill="x")
tk.Button(panel, text="Button", command=lambda: pick_tool("button")).pack(fill="x")
tk.Button(panel, text="Wire", command=lambda: pick_tool("wire")).pack(fill="x")

# Voltage Scale
volts = tk.DoubleVar(value=5)
voltage_label = tk.Label(panel, text=f"Voltage: {volts.get()}")
voltage_label.pack()

def adjust_label(value):
    voltage_label.config(text=f"Voltage: {value}")
    print(f"Volts: {value}")

tk.Scale(panel, from_=1.5, to=24, resolution=0.5,
         orient="horizontal", variable=volts, showvalue=False, command=adjust_label).pack()
#--------------

def redraw():
    canvas.delete("part")
    for a, b in circuit.wires:
        x1, y1 = hole_pos[a]
        x2, y2 = hole_pos[b]
        canvas.create_line(x1, y1, x2, y2, fill="black", tags="part", width=4)
    for kind, a, b in circuit.components:
        x1, y1 = hole_pos[a]
        x2, y2 = hole_pos[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        canvas.create_line(x1, y1, x2, y2, fill="black", tags="part", width=4)
        canvas.create_rectangle(mx - 10, my - 10, mx + 10, my + 10, fill=colors[kind], tags="part")
    canvas.tag_raise("hole")

def on_hole_click(event):
    global start
    item = canvas.find_withtag("current")
    if not item or tool == "select":
        return
    hole = hole_at[item[0]]
    if start is None:
        start = hole
        print("first hole:", hole)
        return
    if tool == "wire":
        circuit.add_wire(start, hole)
    else:
        circuit.add_component(tool, start, hole)
    print(circuit.wires, circuit.components)
    redraw()
    start = None

canvas.tag_bind("hole", "<Button-1>", on_hole_click)
canvas.bind("<Motion>", lambda e: None)

def tick():
    root.after(50, tick)
tick()

root.mainloop()

