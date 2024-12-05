import sys
import math

def get_center(in_list):

    center = math.floor(len(in_list)/2)

    return in_list[center]

def find_next(needle, current_list):

    for idx, el in enumerate(current_list):
        if el == needle:
            return idx
    return -1

def check_rules(rules, current_list):

    print(current_list)

    for rule in rules:
        if (idx := find_next(rule[1], current_list)) > -1:
            if find_next(rule[0], current_list[idx:]) > -1:
                print(current_list, rule)
                return False
    return True

def check_lines(lines, rules):

    canidates = []
    for line in lines:
        if check_rules(rules, line):
            canidates.append(line)
    return canidates

def parse_lines(lines):

    rules = []
    inlines = []
    mode = "r"
    for line in lines.splitlines():
        if line == "":
            mode = "i"
            continue
        if mode == "r":
            rules.append([int(i) for i in line.split("|")])
        if mode == "i":
            inlines.append([int(i) for i in line.split(",")])

    return rules, inlines



def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    rules, inlines = parse_lines(lines)

    canidates = check_lines(inlines, rules)
    print(canidates)
    res = 0
    for canidate in canidates:
        res += get_center(canidate)

    print("Result:", res)



if __name__ == "__main__":
    main(sys.argv[1:])
