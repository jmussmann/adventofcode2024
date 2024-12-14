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

def simulate(robot, seconds):
    for i in range(0, seconds):

        robot.sim_step()
        #print(f"After {i} seconds")
        #robot.print_field_pos()


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
    for robot in robots:
        simulate(robot, int(argv[3]))
    quadrants = count_quadrants(robots, field)
    for el in quadrants:
        res *= el 
    print(res)



if __name__ == "__main__":
    main(sys.argv[1:])
