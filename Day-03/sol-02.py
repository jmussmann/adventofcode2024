import sys
import re

PATTERN = re.compile(r"(mul\((\d*),(\d*)\))")


def process_line(line):

    parts = line.split("do()")
    parts2 = []
    for p in parts:
        parts2.append(p.split("don't()")[0])

    res = 0

    for p in parts2:
        matches = PATTERN.findall(p)
        for match in matches:
             res += int(match[1]) * int(match[2])

    return res

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    print("Result: ", process_line(lines))

if __name__ == "__main__":
    main(sys.argv[1:])
