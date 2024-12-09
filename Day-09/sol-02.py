import sys

def create_layout(line):
    
    el_id = 0
    res = []
    for idx, el in enumerate(line):
        if idx % 2 == 0:
            wr = str(el_id)
            el_id += 1
        else:
            wr = "."
        for _ in range(int(el)):
            res.append(wr)
    return res

def find_block_end(layout, blk_id, idx):

    for i in range(idx-1, -1, -1):
        if blk_id != layout[i]:
            return i+1

    return -1

def find_fitting_block(layout, size):

    free_size = 0
    for i in range(0, len(layout)):
        if layout[i] == ".":
            free_size += 1
        else:
            if size <= free_size:
                return i-free_size
            free_size = 0
    return -1



def defrag(layout):
    i = len(layout)-1
    prev_id = None
    while i > 0:
        if layout[i] == ".":
            i -= 1
            continue
        blk_end = find_block_end(layout, layout[i], i)
        current_id = int(layout[i])
        space_needed = i-blk_end+1
        i = blk_end
        if prev_id is not None and prev_id < current_id:
            i -= 1
            continue
        start_copy = find_fitting_block(layout, space_needed)
        if start_copy == -1 or start_copy >= i:
            prev_id = current_id
            i -= 1
            continue
        for j in range(0, space_needed):
            k = start_copy+j
            if layout[k] == ".":
                layout[i+j], layout[k] = layout[k], layout[i+j]
        prev_id = current_id
        i -= 1

def calc_checksum(layout):

    res = 0
    for idx, el in enumerate(layout):
        if el == ".":
           continue
        res += idx * int(el)

    return res


def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    line = lines.splitlines()[0]

    layout = create_layout(line)

    defrag(layout)
     
    res = calc_checksum(layout)

    print("Result: ", res)

if __name__ == "__main__":
    main(sys.argv[1:])
