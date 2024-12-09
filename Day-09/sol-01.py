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


def defrag(layout):
    search_free_space_start = 0
    stop = False
    for i in range(len(layout)-1, -1,-1):
        if stop:
            break
        if layout[i] == ".":
            continue
        for j in range(search_free_space_start, len(layout)):
            if layout[j] == ".":
                if i < j:
                    stop = True
                    break
                layout[i], layout[j] = layout[j], layout[i]
                search_free_space_start = j+1
                break

def calc_checksum(layout):

    res = 0
    for idx, el in enumerate(layout):
        if el == ".":
            break
        res += idx * int(el)

    return res


def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    line = lines.splitlines()[0]

    layout = create_layout(line)

    #print("".join(layout))

    defrag(layout)
     
    #print(":".join(layout))

    res = calc_checksum(layout)

    print("Result: ", res)

if __name__ == "__main__":
    main(sys.argv[1:])
