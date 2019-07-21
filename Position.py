class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Position({self.x:.3f}, {self.y:.3f})"

    def copy(self):
        obj = Position(self.x, self.y)
        return obj