import sys
import numpy as np

def main(argv):

    locationIds1 = []
    locationIds2 = []
    
    with open(argv[0], "r") as fd:
        lines = fd.read()

    for line in lines.splitlines():
        x, y = line.split("   ")
        locationIds1.append(int(x))
        locationIds2.append(int(y))

    locationsCount = {}
    for el in locationIds2:
        locationsCount[el] = locationsCount.get(el, 0) + 1

    similarity_score = 0
    for el in locationIds1:
        similarity_score += el*locationsCount.get(el, 0)

    print(similarity_score)


if __name__ == "__main__":
    main(sys.argv[1:])
