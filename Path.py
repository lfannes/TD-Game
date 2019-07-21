import Position
import numpy
import util

class Waypoint:
    def __init__(self, pos, time):
        self.pos = pos.copy()
        self.time = time

    def __repr__(self):
        return f"Waypoint({self.pos}, {self.time})"


class Path:
    def __init__(self):
        self.waypoints = list()

    def __repr__(self):
        return f"{self.waypoints}"

    def max_time(self):
        last_waypoint_time = 0
        if self.waypoints:
            last_waypoint_time = self.waypoints[-1].time
        return last_waypoint_time

    def add(self, pos, dt):
        time = self.max_time() + dt
        self.waypoints.append(Waypoint(pos, time))

    def get_pos(self, time):
        if time < 0:
            return None

        if len(self.waypoints) <= 1:
            return None

        a, b = None, None
        for wp in self.waypoints:
            if b is None:
                b = wp
                continue
            a = b
            b = wp
            if a.time <= time and time <= b.time:
                x = util.interpol(a.time, a.pos.x, b.time, b.pos.x, time)
                y = util.interpol(a.time, a.pos.y, b.time, b.pos.y, time)
                return Position.Position(x, y)

        return None


if __name__ == '__main__':
    path = Path()
    pos = Position.Position(50 , 50)
    path.add(pos, 0)
    pos.x += 10
    pos.y += 18
    path.add(pos, 0.3)
    pos.y += 50
    path.add(pos, 0.2)
    print(path)

    for time in numpy.arange(-0.1, path.max_time()+0.001, 0.001):
        print(f"{time:.3f}: {path.get_pos(time)}")