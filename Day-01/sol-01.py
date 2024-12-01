import sys

def main(argv):

    locationIds1 = []
    locationIds2 = []
    
    with open(argv[0], "r") as fd:
        lines = fd.read()

    for line in lines.splitlines():
        x, y = line.split("   ")
        locationIds1.append(int(x))
        locationIds2.append(int(y))

    locationIds1.sort()
    locationIds2.sort()

    res = sum([ abs(x-y) for x, y in zip(locationIds1,locationIds2)])
    print(res)

if __name__ == "__main__":
    main(sys.argv[1:])
