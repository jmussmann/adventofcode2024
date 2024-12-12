import sys

def print_ids(area_map):
    for y_el in area_map.values():
        print("\t".join([str(el) for el in y_el.values()]))

def parse_lines(lines):

    field = []
    for line in lines.splitlines():
        field.append(list(line))

    return field, len(field[0]), len(field)

def set_fence(fences, area_id, x_pos, y_pos, corner):
    #UDLR -> 4bits
    #1111 -> 4bits
    if area_id not in fences:
        fences[area_id] = {}
    if y_pos not in fences[area_id]:
        fences[area_id][y_pos] = {}
    if x_pos not in fences[area_id][y_pos]:
        fences[area_id][y_pos][x_pos] = 0b0000
    fences[area_id][y_pos][x_pos] |= corner

def process_positions(x_pos, y_pos, x_dim, y_dim, field, fences, area, area_map, area_id):

    el = field[y_pos][x_pos]
    
    if y_pos in area_map and x_pos in area_map[y_pos]:
        return

    if y_pos not in area_map:
        area_map[y_pos] = {}

    area_map[y_pos][x_pos] = area_id

    area[area_id] = area.get(area_id, 0) + 1
    if x_pos - 1 < 0 or el != field[y_pos][x_pos-1]:
        set_fence(fences, area_id, x_pos, y_pos, 0b0010)
    else:
        process_positions(x_pos-1, y_pos, x_dim, y_dim, field, fences, area, area_map, area_id)
    if y_pos - 1 < 0 or el != field[y_pos-1][x_pos]:
        set_fence(fences, area_id, x_pos, y_pos, 0b1000)
    else:
        process_positions(x_pos, y_pos-1, x_dim, y_dim, field, fences, area, area_map, area_id)
    if x_pos + 1 >= x_dim or el != field[y_pos][x_pos+1]:
        set_fence(fences, area_id, x_pos, y_pos, 0b0001)
    else:
        process_positions(x_pos+1, y_pos, x_dim, y_dim, field, fences, area, area_map, area_id)
    if y_pos + 1 >= y_dim or el != field[y_pos+1][x_pos]:
        set_fence(fences, area_id, x_pos, y_pos, 0b0100)
    else:
        process_positions(x_pos, y_pos+1, x_dim, y_dim, field, fences, area, area_map, area_id)

    return

def process_fence(area_id, y_pos, x_pos, fences):

    area_fences = fences[area_id]

    
    if fences[area_id][y_pos][x_pos] & 0b0011 > 0:
        y_next = -1
        prev_x_or = fences[area_id][y_pos][x_pos] 
        while y_pos+y_next in area_fences and x_pos in area_fences[y_pos+y_next]:
            save = fences[area_id][y_pos+y_next][x_pos]
            fences[area_id][y_pos+y_next][x_pos] &= (0b1100 | (prev_x_or ^ fences[area_id][y_pos+y_next][x_pos]))
            y_next -= 1
            prev_x_or = save
        y_next = 1
        prev_x_or = fences[area_id][y_pos][x_pos] 
        while y_pos+y_next in area_fences and x_pos in area_fences[y_pos+y_next]:
            save = fences[area_id][y_pos+y_next][x_pos]
            fences[area_id][y_pos+y_next][x_pos] &= (0b1100 | (prev_x_or^ fences[area_id][y_pos+y_next][x_pos]))
            y_next += 1
            prev_x_or = save
    if fences[area_id][y_pos][x_pos] & 0b1100 > 0:
        x_next = -1
        prev_x_or = fences[area_id][y_pos][x_pos] 
        while y_pos in area_fences and x_pos+x_next in area_fences[y_pos]:
            save = fences[area_id][y_pos][x_pos+x_next]
            fences[area_id][y_pos][x_pos+x_next] &= (0b0011 | (prev_x_or ^ fences[area_id][y_pos][x_pos+x_next]))
            x_next -= 1
            prev_x_or = save
        x_next = 1
        prev_x_or = fences[area_id][y_pos][x_pos] 
        while y_pos in area_fences and x_pos+x_next in area_fences[y_pos]:
            save = fences[area_id][y_pos][x_pos+x_next]
            fences[area_id][y_pos][x_pos+x_next] &= (0b0011 | (prev_x_or ^ fences[area_id][y_pos][x_pos+x_next]))
            x_next += 1
            prev_x_or = save

def process_fence_parts(fences):
    fence_parts = {}
    for area_id, area in fences.items():
        for y_pos, fence_x in area.items():
            for x_pos, fence_part in fence_x.items():
                if fence_part == 0:
                    continue
                process_fence(area_id, y_pos, x_pos, fences)

                fence_parts[area_id] = fence_parts.get(area_id, 0) + bin(fence_part).count('1')
    return fence_parts




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
    fence_parts = process_fence_parts(fences)

    

    print("Result: ", get_sol(area, fence_parts))

if __name__ == "__main__":
    main(sys.argv[1:])
