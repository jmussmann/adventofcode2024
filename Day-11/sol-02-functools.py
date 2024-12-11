import sys
import math
from functools import cache

@cache
def process_element(el, blink=0, n_blinks=25):
    global MAP
    if blink == n_blinks:
        return 1
    if el == 0:
        return process_element(1, blink+1, n_blinks)
    n_digets = math.floor(math.log10(el)) + 1
    if n_digets % 2 == 0:
        upper = int(el/10**(n_digets/2))
        lower = int(el - upper*10**(n_digets/2))
        return process_element(upper, blink+1, n_blinks) + process_element(lower, blink+1, n_blinks)

    return process_element(el*2024, blink+1, n_blinks)


def blinks(line, n_blinks):
    
    res = 0
    line = [int(el) for el in line]
    for el in line:
        res += process_element(el, 0, n_blinks)
    return res

def main(argv):

    with open(argv[0], "r") as fd:
        line = fd.read()

    line = line.strip()
    line = line.split(" ")


    res = blinks(line, int(argv[1]))

    print("Result: ", res)

if __name__ == "__main__":
    main(sys.argv[1:])
