import sys
import re

PATTERN = re.compile(r"(mul\((\d*),(\d*)\))")

def process_line(line):


    matches = PATTERN.findall(line)

    res = 0
    for match in matches:
        res += int(match[1]) * int(match[2])

    return res

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    print("Result: ", process_line(lines))

if __name__ == "__main__":
    main(sys.argv[1:])
