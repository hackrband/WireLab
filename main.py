import tkinter as tk

root = tk.Tk()
root.title("WireLab")

root.geometry("900x400")

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

        holes[(col, row)] = canvas.create_oval(
            x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="#bcc7bf", tags="hole"
        )

# -----------------

def pick_tool(name):
    print("tool:", name)

#def adjust_voltage(volts):
#    print("voltage:", volts)

tk.Button(panel, text="LED", command=lambda: pick_tool("led")).pack(fill="x")
tk.Button(panel, text="Resistor", command=lambda: pick_tool("resistor")).pack(fill="x")
tk.Button(panel, text="Capacitor", command=lambda: pick_tool("capacitor")).pack(fill="x")
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

canvas.tag_bind("hole", "<Button-1>", lambda e: print("clicked", e.x, e.y))
canvas.bind("<Motion>", lambda e: None)

def tick():
    root.after(50, tick)
tick()

root.mainloop()

