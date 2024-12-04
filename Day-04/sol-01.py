import sys

def process_lines(lines):

    res = 0
    for i, line in enumerate(lines):
        for j, el in enumerate(line):
            if el != "X":
                continue
            if j < len(line) - 3 and line[j:j+4] == "XMAS":
                res += 1
            if j > 2 and line[j-3:j+1] == "SAMX":
                res += 1
            if i < len(lines)-3 and j < len(line) - 3:
                ok = True
                for k, c in enumerate("XMAS"):
                    if lines[i+k][j+k] != c:
                        ok = False
                        break
                if ok:
                    res += 1
            if i < len(lines)-3 and j > 2:
                ok = True
                for k, c in enumerate("XMAS"):
                    if lines[i+k][j-k] != c:
                        ok = False
                        break
                if ok:
                    res += 1

            if i > 2 and j < len(line) - 3:
                ok = True
                for k, c in enumerate("XMAS"):
                    if lines[i-k][j+k] != c:
                        ok = False
                        break
                if ok:
                    res += 1
            if i > 2 and j > 2:
                ok = True
                for k, c in enumerate("XMAS"):
                    if lines[i-k][j-k] != c:
                        ok = False
                        break
                if ok:
                    res += 1
            if i > 2:
                ok = True
                for k, c in enumerate("XMAS"):
                    if lines[i-k][j] != c:
                        ok = False
                        break
                if ok:
                    res += 1
            if i < len(lines)-3:
                ok = True
                for k, c in enumerate("XMAS"):
                    if lines[i+k][j] != c:
                        ok = False
                        break
                if ok:
                    res += 1
    return res

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    print("Result: ", process_lines(lines.splitlines()))

if __name__ == "__main__":
    main(sys.argv[1:])
