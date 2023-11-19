import os
from math import sqrt


def clear():
    os.system("cls||clear")


class QuadRoute:
    """
    Basic class of a quadcopter route.
    """
    AREA = ([0, 100], [0, 100])
    START = []
    END = []
    TRANSMITTERS = []
    ROUTES_GRAPH = {}

    def set_start(self, start: list[int, int]):
        if self._in_area_range(start):
            self.START = start
            print(f"Starting point was successfully set to: {start}")

    def set_end(self, end: list[int, int]):
        if self._in_area_range(end):
            self.END = end
            print(f"Ending point was successfully set to: {end}")

    def _in_area_range(self, point) -> bool:
        if type(point[0]) is not int or type(point[1]) is not int:
            print("Coordinate must be an integer")
            return False
        if point[0] < self.AREA[0][0] or point[0] > self.AREA[0][1]:
            print("X-Coordinate is outside the route area")
            return False
        if point[1] < self.AREA[1][0] or point[1] > self.AREA[1][1]:
            print("Y-Coordinate is outside the route area")
            return False
        return True

    @staticmethod
    def _check_area_coordinates(area: tuple[list[int, int], list[int, int]]) -> bool:
        for coordinates in area:
            if coordinates[0] > coordinates[1]:
                print("Second coordinate must be equal or greater than the first one")
                return False
            for coordinate in coordinates:
                if type(coordinate) is not int or coordinate < 0:
                    print("Every coordinate must be a positive integer")
                    return False
        return True

    def set_area_coordinates(self, area):
        if self._check_area_coordinates(area):
            self.AREA = area
            print(f"Area coordinates were successfully set to: {area}")

    def _check_transmitter_values(self, transmitter) -> bool:
        if not self._in_area_range(transmitter):
            print(f"Transmitter with values: {transmitter} is outside the route area")
            return False
        if len(transmitter) != 3:
            print("Transmitter should have 3 values: X-coordinate, Y-coordinate and power")
            return False
        if type(transmitter[2]) is not int or transmitter[2] < 0:
            print("The power value of a transmitter should be a positive integer")
            return False
        if transmitter in self.TRANSMITTERS:
            print(f"Transmitter with values: {transmitter} is among already added transmitters")
            return False
        return True

    def add_transmitter(self, transmitter: tuple[int, int, int]):
        if self._check_transmitter_values(transmitter):
            self.TRANSMITTERS.append(transmitter)
            print(f"Transmitter with values: {transmitter} was added successfully")

    def _in_transmitter_range(self, point: list[int, int]):
        for t in self.TRANSMITTERS:
            if sqrt((t[0] - point[0])**2 + (t[1] - point[1])**2) <= t[2]:
                return t
        return None

    def check_starting_and_ending_points(self):
        if self.START and self.END:
            if self._in_transmitter_range(self.START) and self._in_transmitter_range(self.END):
                print(f"Starting and ending points are inside a transmitters range")
                return True
            print(f"Starting and ending points are outside any of given transmitters range")
        else:
            print(f"You have to set both of starting and ending points")
        return False

    def create_routes_graph(self):
        graph = {}
        for t1 in self.TRANSMITTERS:
            graph[t1] = []
            for t2 in self.TRANSMITTERS:
                if t1 != t2:
                    if sqrt((t1[0] - t2[0])**2 + (t1[1] - t2[1])**2) <= (t1[2] + t2[2]):
                        graph[t1].append(t2)
        self.ROUTES_GRAPH = graph.copy()

    def find_path(self, start, end, path=None):
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.ROUTES_GRAPH:
            return None

        paths = []
        for node in self.ROUTES_GRAPH[start]:
            if node not in path:
                new_paths = self.find_path(node, end, path)
                for p in new_paths:
                    paths.append(p)
        return paths

    def check_for_save_route(self):
        if self.check_starting_and_ending_points():
            self.create_routes_graph()
            t_start = self._in_transmitter_range(self.START)
            t_end = self._in_transmitter_range(self.END)
            paths = self.find_path(t_start, t_end)
            if paths:
                print(f"There is a save path for quadrocopter:")
                for p in paths:
                    print(p)
                return
        print(f"There is NO save route for a given start and end points within given transmitters")

    def get_all_transmitters(self):
        return self.TRANSMITTERS

    @staticmethod
    def _print_menu_options():
        clear()
        print(f"1. Set the area coordinates")
        print(f"2. Add new transmitter")
        print(f"3. Get all transmitters")
        print(f"4. Set a starting point")
        print(f"5. Set an ending point")
        print(f"6. Check for a save path for quadrocopter")
        print(f"0. Exit")

    def menu(self):
        while True:
            self._print_menu_options()
            key = input(f"\nChoose option: ")
            if key == "1":
                x = input(f"Set X-coordinates for area in the format 'x_min x_max': ").split()
                y = input(f"Set Y-coordinates for area in the format 'y_min y_max': ").split()
                self.set_area_coordinates(([int(i) for i in x], [int(i) for i in y]))
            elif key == "2":
                val = input(f"Set values for a new transmitter in the format 'x y p': ").split()
                values = tuple([int(x) for x in val])
                self.add_transmitter(transmitter=values)
            elif key == "3":
                print(self.get_all_transmitters())
            elif key == "4":
                val = input(f"Set values for starting point in the format 'x y': ").split()
                values = [int(x) for x in val]
                self.set_start(start=values)
            elif key == "5":
                val = input(f"Set values for ending point in the format 'x y': ").split()
                values = [int(x) for x in val]
                self.set_end(end=values)
            elif key == "6":
                self.check_for_save_route()
            elif key == "0":
                break
            else:
                print(f"You have chosen an invalid option: '{key}'")
            input(f"\nPress any key to get back to menu")


if __name__ == "__main__":
    route = QuadRoute()
    route.menu()

