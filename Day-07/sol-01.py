import sys

def parse_lines(lines):

    results = []
    numbers = []
    for line in lines.splitlines():
        line_result, line_numbers = line.split(":")
        line_result = int(line_result)
        line_numbers = [ int(n) for n in line_numbers.split(" ")[1:] ]

        results.append(line_result)
        numbers.append(line_numbers)

    return results, numbers

def process_line(result, numbers, operator, res):

    if len(numbers) == 0:
        return res

    in_res = res
    if operator == "+":
        res = process_line(result, numbers[1:], "+", in_res + numbers[0])
        if res != result:
            res = process_line(result, numbers[1:], "*", in_res + numbers[0])
    if operator == "*":
        res = process_line(result, numbers[1:], "+", in_res * numbers[0])
        if res != result:
            res = process_line(result, numbers[1:], "*", in_res * numbers[0])

    return res

def process_lines(results, numbers):

    res = 0
    for result, nums in zip(results, numbers):

        if process_line(result, nums, "+", 0) == result or process_line(result, nums, "*", 1) == result:
            res += result

    return res

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    results, numbers = parse_lines(lines)


    print("Result: ", process_lines(results, numbers))

if __name__ == "__main__":
    main(sys.argv[1:])
