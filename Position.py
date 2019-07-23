import math

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Position({self.x:.3f}, {self.y:.3f})"

    def copy(self):
        obj = Position(self.x, self.y)
        return obj

    def overPos(self, pos):
        if self.x >= pos.x or self.y > pos.y:
            return True
        else:
            return False

    def distance(self, pos):
        distance = math.sqrt((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2)
        return distance