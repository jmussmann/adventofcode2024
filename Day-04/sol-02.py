import sys

def process_lines(lines):

    res = 0
    for i, line in enumerate(lines):
        for j, el in enumerate(line):
            if el != "A":
                continue
            if i > 0 and i < len(lines)-1 and j > 0 and j < len(line) - 1:
                diag1 = ""
                diag2 = ""
                for k in range(0, 3):
                    diag1 += lines[i-1+k][j-1+k] 
                    diag2 += lines[i+1-k][j-1+k] 

                if (diag1 == "MAS" or diag1 == "SAM") and (diag2 == "MAS" or diag2 == "SAM"):
                    res += 1
    return res



def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    print("Result: ", process_lines(lines.splitlines()))

if __name__ == "__main__":
    main(sys.argv[1:])
