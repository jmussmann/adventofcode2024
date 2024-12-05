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


def sort_rules(rules):

    for idx in range(len(rules)):
        for idx2 in range(idx+1, len(rules[idx:])):
            if rules[idx][1] == rules[idx2][0]:
                rules[idx], rules[idx2] = rules[idx2], rules[idx]



def reorder(current_list, rules):
    for rule in rules:
        if (idx := find_next(rule[1], current_list)) > -1:
            while (idx2 := find_next(rule[0], current_list[idx:])) > -1:
                el = current_list.pop(idx2+idx)
                current_list.insert(idx, el)
                idx = idx2+idx



def check_rules(rules, current_list):

    matched_rules = []
    do_sort = False
    for rule in rules:
        if (idx := find_next(rule[1], current_list)) > -1:
            matched_rules.append(rule)
            if find_next(rule[0], current_list[idx:]) > -1:
                do_sort = True
    if do_sort:
        sort_rules(matched_rules)
        reorder(current_list, matched_rules)
        return True
    return False

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
    res = 0
    # Unfortunately sorting the rules is not as easy as i thought
    # So looping until everything is correct:
    while (len(check_lines(inlines, rules)) > 0):
        pass
    for canidate in canidates:
        res += get_center(canidate)

    print("Result:", res)



if __name__ == "__main__":
    main(sys.argv[1:])
