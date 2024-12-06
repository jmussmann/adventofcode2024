import sys
import os

def clear():
    os.system('clear')

def print_field(field):
    clear()
    for line in field:
        print(''.join(line))

def count_X(field):

    res = 0
    for line in field:
        for el in line:
            if el == "X":
                res += 1
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


def simulate(field, start):

    position = start

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
    print_field(field)



def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    field, start  = parse_lines(lines)

    simulate(field, start)
    print(count_X(field))



if __name__ == "__main__":
    main(sys.argv[1:])
