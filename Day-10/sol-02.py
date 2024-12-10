import sys

def parse_lines(lines):

    field = []
    for line in lines.splitlines():
        field_line = []
        for el in line:
            if el == ".":
                el = 42
            field_line.append(int(el))
        field.append(field_line)

    return field

def filter_0(line):
    
    res = []
    for idx, el in enumerate(line):
        if el == 0:
           res.append(idx) 

    return res

def get_next_positions(x_pos, y_pos, next_num, field):

    res = []

    if x_pos - 1 > -1:
        pos = (x_pos-1, y_pos)
        if next_num == field[pos[1]][pos[0]]:
            res.append(pos)
    if y_pos - 1 > -1:
        pos = (x_pos, y_pos-1)
        if next_num == field[pos[1]][pos[0]]:
            res.append(pos)
    if x_pos + 1 < len(field[0]):
        pos = (x_pos+1, y_pos)
        if next_num == field[pos[1]][pos[0]]:
            res.append(pos)
    if y_pos + 1 < len(field):
        pos = (x_pos, y_pos+1)
        if next_num == field[pos[1]][pos[0]]:
            res.append(pos)

    return res

def step(x_pos, y_pos, num, field):
    
    res = 0
    if num < 9:
        next_num = num+1
        next_positions = get_next_positions(x_pos, y_pos, next_num, field)
        for pos in next_positions:
            res += step(pos[0], pos[1], num+1, field)
    else:
        res = 1

    return res

def process_field(field):

    res = 0
    for y_pos, line in enumerate(field):
        zeros = filter_0(line)
        for zero_x_pos in zeros:
            t = step(zero_x_pos, y_pos, 0, field)
            res += t #step(zero_x_pos, y_pos, 0, field)
    return res

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    field = parse_lines(lines)

    print("Result: ", process_field(field))

if __name__ == "__main__":
    main(sys.argv[1:])
