import sys
import os
import pprint
import copy

def clear():
    os.system('clear')

def print_field(field):
    for line in field:
        print(''.join(line))

def get_x_pos(field):

    res = []
    for idx, line in enumerate(field):
        for idx2, el in enumerate(line):
            if el == "X":
                res.append([idx, idx2])
    return res

def parse_lines(lines):

    field = []
    start = [-1, -1]
    for idx, line in enumerate(lines.splitlines()):
        field.append(list(line))
        if (idx2 := line.find("^")) > -1:
            start = [idx, idx2]

    return field, start

def add(a, b):

    return [a[0] + b[0], a[1]+b[1]]

def get_field(A, x):

    return A[x[0]][x[1]]

def check_pos(position, field):
    return position[0] > -1 and position[0] < len(field) and position[1] > -1 and position[1] < len(field[0])

def set_field(A, x, v):

    A[x[0]][x[1]] = v


def simulate(field, start, path):


    direction_map = {
        "^": [-1, 0],
        "v": [1, 0],
        "<": [0, -1],
        ">": [0, 1],
    }
    turn_map = {
        "^": ">",
        "v": "<",
        "<": "^",
        ">": "v",
    }

    res = 0

    for i, element in enumerate(path):
        print("{}/{}".format(i, len(path)))
        position = start
        visited_map = {}
        field_tmp = copy.deepcopy(field)
        direction = "^"
        set_field(field_tmp, element, "O")

        next_position = add(position, direction_map[direction])
        while next_position[0] > -1 and next_position[0] < len(field) and next_position[1] > -1 and next_position[1] < len(field[0]):

            if position[0] not in visited_map:
                visited_map[position[0]] = {}
            if position[1] not in visited_map[position[0]]:
                visited_map[position[0]][position[1]] = []
            if direction in visited_map[position[0]][position[1]]:
                res += 1
                break
            visited_map[position[0]][position[1]].append(direction)
            if get_field(field_tmp, next_position) == "#" or get_field(field_tmp, next_position) == "O":
                direction = turn_map[direction]
            else:
                position = next_position
            next_position = add(position, direction_map[direction])

    return res

def build_path(field, start):

    position = start
    field.copy()

    direction_map = {
        "^": [-1, 0],
        "v": [1, 0],
        "<": [0, -1],
        ">": [0, 1],
    }
    turn_map = {
        "^": ">",
        "v": "<",
        "<": "^",
        ">": "v",
    }
    direction = "^"

    next_position = add(position, direction_map[direction])
    while next_position[0] > -1 and next_position[0] < len(field) and next_position[1] > -1 and next_position[1] < len(field[0]):

        set_field(field, position, "X")
        if get_field(field, next_position) == "#":
            direction = turn_map[direction]
        else:
            position = next_position
        next_position = add(position, direction_map[direction])

    set_field(field, position, "X")

    return field

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    field, start = parse_lines(lines)
    field_with_path = build_path(field, start)

    x_pos = get_x_pos(field_with_path)

    res = simulate(field, start, x_pos)
    print(res)



if __name__ == "__main__":
    main(sys.argv[1:])
