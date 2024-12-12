import sys

def print_ids(area_map):
    for y_el in area_map.values():
        print("\t".join([str(el) for el in y_el.values()]))

def parse_lines(lines):

    field = []
    for line in lines.splitlines():
        field.append(list(line))

    return field, len(field[0]), len(field)

def process_positions(x_pos, y_pos, x_dim, y_dim, field, fences, area, area_map, area_id):

    el = field[y_pos][x_pos]
    
    if y_pos in area_map and x_pos in area_map[y_pos]:
        return

    if y_pos not in area_map:
        area_map[y_pos] = {}

    area_map[y_pos][x_pos] = area_id

    area[area_id] = area.get(area_id, 0) + 1
    if x_pos - 1 < 0 or el != field[y_pos][x_pos-1]:
        fences[area_id] = fences.get(area_id, 0) + 1
    else:
        process_positions(x_pos-1, y_pos, x_dim, y_dim, field, fences, area, area_map, area_id)
    if y_pos - 1 < 0 or el != field[y_pos-1][x_pos]:
        fences[area_id] = fences.get(area_id, 0) + 1
    else:
        process_positions(x_pos, y_pos-1, x_dim, y_dim, field, fences, area, area_map, area_id)
    if x_pos + 1 >= x_dim or el != field[y_pos][x_pos+1]:
        fences[area_id] = fences.get(area_id, 0) + 1
    else:
        process_positions(x_pos+1, y_pos, x_dim, y_dim, field, fences, area, area_map, area_id)
    if y_pos + 1 >= y_dim or el != field[y_pos+1][x_pos]:
        fences[area_id] = fences.get(area_id, 0) + 1
    else:
        process_positions(x_pos, y_pos+1, x_dim, y_dim, field, fences, area, area_map, area_id)

    return

def process_field(field, x_dim, y_dim):

    fences = {}
    area = {}
    area_map = {}
    current_max_area_id = 0
    for y_pos in range(0, y_dim):
        for x_pos in range(0, x_dim):
            process_positions(x_pos, y_pos, x_dim, y_dim, field, fences, area,area_map, current_max_area_id)
            current_max_area_id += 1


    return fences, area

def get_sol(area, fences):

    res = 0
    for k, v in area.items():
        res += fences.get(k, 0) * v

    return res

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    field, x_dim, y_dim = parse_lines(lines)

    fences, area = process_field(field, x_dim, y_dim)
    

    print("Result: ", get_sol(area, fences))

if __name__ == "__main__":
    main(sys.argv[1:])
