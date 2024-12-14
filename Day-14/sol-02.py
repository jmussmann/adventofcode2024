import sys
import re
from copy import deepcopy

class vec2:

    def __init__(self, x, y):

        self.x = int(x)
        self.y = int(y)

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

    __rmul__ = __mul__

    def __div__(self, other):

        if isinstance(other, int) or isinstance(other, float):
            return vec2(self.x / other, self.y / other)
        raise NotImplementedError

    def __str__(self):

        return f"vec2({self.x}, {self.y})"

class Robot:

    def __init__(self, pos, velocity, field):

        self.pos = pos
        self.v = velocity
        self.field = field

    def sim_step(self):

        next_pos = self.pos + self.v

        next_pos.x = next_pos.x % self.field.x
        next_pos.y = next_pos.y % self.field.y

        self.pos = next_pos


    def __str__(self):

        return f"Robot(pos:{self.pos}, v: {self.v})"

    def print_field_pos(self):

        for y in range(0, self.field.y):
            to_print = []
            for x in range(0, self.field.x):
                if self.pos.x == x and self.pos.y == y:
                    to_print.append("X")
                else:
                    to_print.append(".")

            print("".join(to_print))

def print_all_robots(robots, field):
    for y in range(0, field.y):
        to_print = []
        for x in range(0, field.x):
            el = "."
            for robot in robots:
                if robot.pos.x == x and robot.pos.y == y:
                    el = "X"
                    break
            to_print.append(el)


        print("".join(to_print))

def all_robot_positions(robots, field):
    lines = []
    for y in range(0, field.y):
        line = []
        for x in range(0, field.x):
            el = "."
            for robot in robots:
                if robot.pos.x == x and robot.pos.y == y:
                    el = "X"
                    break
            line.append(el)
        lines.append(line)

    return lines

def print_robot_positions(robot_positions):
    for y in robot_positions:
        print("".join(y))


def check_christmas_tree(x_pos, y_pos, robot_positions, field):

    pattern = [
        [".", ".", "X", ".", "."],
        [".", "X", "X", "X", "."],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]

    for i in range(-2, 3, 1):
        if y_pos + i < 0 or y_pos + i > field.y-1:
            return False
        for j in range(-2, 3, 1):
            if x_pos + j < 0 or x_pos + j > field.x-1:
                return False
            if pattern[2+i][2+j] != robot_positions[y_pos+i][x_pos+j]:
                return False

    return True




def search_christmas_tree(robot_positions, field):

    for y in range(0, field.y):
        for x in range(0, field.x):
            if check_christmas_tree(x, y, robot_positions, field):
                return True
                
    return False


def simulate(robots, seconds, field):
    print_all_robots(robots, field)
    res = 0
    for i in range(1, seconds):
        if i % 10 == 0:
            print(f"{i}/{seconds}")
        for robot in robots:
            robot.sim_step()
        field_map = all_robot_positions(robots, field)
        if search_christmas_tree(field_map, field):
            res = i
            print(f"After {i} seconds")
            print_all_robots(robots, field)
            break
    return res


def parse_lines(lines, field):

    pos_regex = re.compile(r"p=(\d+),(\d+)")
    velocity_regex = re.compile(r"v=(-?\d+),(-?\d+)")

    robots = []
    for line in lines.splitlines():
        pos_match = pos_regex.search(line)
        velocity_match = velocity_regex.search(line)

        pos = vec2(int(pos_match.group(1)), int(pos_match.group(2)))
        velocity = vec2(int(velocity_match.group(1)), int(velocity_match.group(2)))
        robots.append(Robot(pos, velocity, field))
        

    return robots

def get_quadrant(robot, field):

    field_2 = (field -vec2(1,1)) *0.5 
    if robot.pos.x < field_2.x and robot.pos.y < field_2.y:
        return 0 
    if robot.pos.x > field_2.x and robot.pos.y < field_2.y:
        return 1 
    if robot.pos.x < field_2.x and robot.pos.y > field_2.y:
        return 2 
    if robot.pos.x > field_2.x and robot.pos.y > field_2.y:
        return 3 
    return -1

def count_quadrants(robots, field):

    quadrants = [0, 0,
                0 ,0]
    for robot in robots:
        if (idx := get_quadrant(robot, field)) != -1:
            quadrants[idx] += 1

    return quadrants


def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()
    field = vec2(int(argv[1]), int(argv[2]))
    robots = parse_lines(lines, field)
    res = 1
    res = simulate(robots, int(argv[3]), field)
    print(res)



if __name__ == "__main__":
    main(sys.argv[1:])
