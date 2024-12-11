import sys

def process_element(el):
    print(el, len(el))

    iel = int(el)
    if iel == 0:
        return [str(1)]
    if len(el) % 2 == 0:
        el1, el2 = el[:int(len(el)/2)],el[int(len(el)/2):] 
        return [str(int(el1)), str(int(el2))]

    return [str(iel * 2024)]


def blink(n_blinks, line):
    new_line = line.copy()

    print(new_line)

    for _ in range(n_blinks):
        old_line = new_line.copy()
        new_line = []
        for el in old_line:
            new_line += process_element(el)
        
        print(new_line)
    return new_line

        

def main(argv):

    with open(argv[0], "r") as fd:
        line = fd.read()

    line = line.strip()
    line = line.split(" ")

    new_line = blink(25, line)


    print("Result: ", len(new_line) )

if __name__ == "__main__":
    main(sys.argv[1:])
