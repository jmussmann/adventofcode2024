import sys

def remove_from_list(elements, idx):
    print(idx)
    elements.pop(idx)
    return elements


def process_elements(elements, depth=0, max_depth=1):
    last = None
    was_inc = None
    if depth > max_depth:
        print("Depth:", depth)
        return False
    else:
        print(elements, "Depth:", depth)
    for idx, el in enumerate(elements):
        el = int(el)
        if last is None:
            last = el
            continue
        diff = el - last
        if abs(diff) > 3 or abs(diff) < 1:
            print("diff")
            if not process_elements(remove_from_list(elements.copy(), idx), depth+1):
                return process_elements(remove_from_list(elements.copy(), idx-1), depth+1)
        last = el
        if diff < 0:
            inc = False
        else:
            inc = True
        if was_inc is None:
            was_inc = inc
            continue
        if inc != was_inc:
            print("Inc")
            if idx == 2:
                if process_elements(remove_from_list(elements.copy(), 0), depth+1):
                    return True
            if not process_elements(remove_from_list(elements.copy(), idx), depth+1):
                return process_elements(remove_from_list(elements.copy(), idx-1), depth+1)
    return True

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    res = 0
    for line in lines.splitlines():
        safe = False
        if safe:= process_elements(line.split(" ")):
            res += 1
        print(line, "->", safe)

    print("Result:", res)

if __name__ == "__main__":
    main(sys.argv[1:])
