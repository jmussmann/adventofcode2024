import sys
import math
class vec2:

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x + other.x, self.y + other.y)
        raise NotImplementedError

    def __sub__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x - other.x, self.y - other.y)
        raise NotImplementedError

    def __mul__(self, other):

        if isinstance(other, int) or isinstance(other, float):
            return vec2(self.x * other, self.y * other)
        raise NotImplementedError

    def __abs__(self):

        return math.sqrt(self.x**2+self.y**2)
    
    def __truediv__(self, other): 

        if isinstance(other, int) or isinstance(other, float):
            return vec2(self.x / other, self.y / other)

    def __str__(self):

        return f"vec2({self.x}, {self.y})"


def parse_lines(lines):

    lines = lines.splitlines()
    y_dim = len(lines)
    x_dim = len(lines[0])
    antennas = {}
    for y_pos, line in enumerate(lines):
        for x_pos, el in enumerate(line):
            if el == ".":
                continue

            if el not in antennas:
                antennas[el] = []

            antennas[el].append(vec2(x_pos, y_pos))

    return x_dim, y_dim, antennas

def check_pos(pos, x_dim, y_dim):
    if math.floor(pos.x) != pos.x:
        return False
    if pos.x > -1 and pos.y > -1 and pos.x < x_dim and pos.y < y_dim:
        return True

    return False

def calculate_intersection(pos, vec, y):

    alpha = (y-pos.y) / vec.y
    x = pos.x + alpha * vec.x

    return vec2(x, y)


def process_antenna(positions, x_dim, y_dim):

    res = []
    
    for idx1, antenna1 in enumerate(positions):
        if idx1 > len(positions)-2:
            break
        for antenna2 in positions[idx1+1:]:
            diff_vec = antenna2 - antenna1

            for y in range(y_dim):
                intersection = calculate_intersection(antenna1, diff_vec, y)
                if check_pos(intersection, x_dim, y_dim):
                    res.append(intersection)
    return res

def process_antennas(antennas, x_dim, y_dim):

    antinodes_map = {}
    res = 0
    for antenna in antennas.values():

        points = process_antenna(antenna, x_dim, y_dim)
        for point in points:
            if point.y not in antinodes_map:
                antinodes_map[point.y] = {}
            if point.x not in antinodes_map[point.y]:
                antinodes_map[point.y][point.x] = 1
                res += 1
    return res


def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    x_dim, y_dim, antennas = parse_lines(lines)


    print("Result: ", process_antennas(antennas, x_dim, y_dim))

if __name__ == "__main__":
    main(sys.argv[1:])
