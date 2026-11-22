class Circuit:
    def __init__(self):
        self.wires = []
        self.components = []

    def add_component(self, kind, a, b):
        if a == b:
            return False
        else:
            self.components.append((kind, a, b))
            return True

    def add_wire(self, a, b):
        if a == b:
            return False
        else:
            self.wires.append((a, b))
            return True

    def clear(self):
        self.wires.clear()
        self.components.clear()

if __name__ == "__main__":
    c = Circuit()
    print(c.add_component("resistor", (3,2), (5,2)))
    print(c.components)
