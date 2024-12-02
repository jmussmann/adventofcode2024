import sys


def process_line(line):
    elements = line.split(" ")

    last = None
    was_inc = None
    for el in elements:
        el = int(el)
        if last is None:
            last = el
            continue
        diff = el - last
        last = el
        if abs(diff) > 3 or abs(diff) < 1:
            print("Diff")
            return False
        if diff < 0:
            inc = False
        else:
            inc = True
        if was_inc is None:
            was_inc = inc
            continue
        if inc != was_inc:
            print("Not inc")
            return False
    return True

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    res = 0
    for line in lines.splitlines():
        safe = False
        if safe := process_line(line):
            res += 1
        print(line, "->", safe)

    print("Result:", res)

if __name__ == "__main__":
    main(sys.argv[1:])
