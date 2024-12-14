import sys
import re
from copy import deepcopy

class vec2:

    def __init__(self, x, y):

        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x + other.x, self.y + other.y)
        raise NotImplementedError

    def __sub__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x - other.x, self.y - other.y)
        raise NotImplementedError

    def __mul__(self, other):

        if isinstance(other, int) or isinstance(other, float):
            return vec2(self.x * other, self.y * other)
        raise NotImplementedError

    __rmul__ = __mul__

    def __str__(self):

        return f"vec2({self.x}, {self.y})"

class ClawMachine:

    def __init__(self, buttonA, buttonB, prize, start=vec2(0,0), max_steps = 100):

        self.buttonA = buttonA
        self.buttonB = buttonB
        self.prize = prize
        self.current_pos = start
        self.current_costs = 0 
        self.win = False
        self.max_steps = max_steps
        self.steps = 0
        self.unwinable = False

    def press_buttonA(self):
        self.current_pos = self.current_pos + self.buttonA
        self.current_costs += 3
        self.steps += 1
        #print(self)

        return self._check_win()

    def press_buttonB(self):
        self.current_pos = self.current_pos + self.buttonB
        self.current_costs += 1
        self.steps += 1
        #print(self)

        return self._check_win()

    def _check_unwinable(self):

        if self.steps >= self.max_steps:
            self.unwinable = True
        if self.current_pos.x > self.prize.x or self.current_pos.y > self.prize.y:
            self.unwinable = True

        return self.unwinable

    def _check_win(self):

        self._check_unwinable()
        if self.current_pos.x == self.prize.x and self.current_pos.y == self.prize.y:
            self.win = True

        return self.win


    def __str__(self):

        return f"ClawMachine({self.buttonA}, {self.buttonB}, {self.current_pos }->{self.prize})"

def simulate_claw_reverse(claw_machine):

    min_cost = 0
    for i in range(0, 100):
        for j in range(0, 100):
            pos = claw_machine.prize - (i * claw_machine.buttonA +j* claw_machine.buttonB)
            if pos.x == 0 and pos.y == 0:
                cost = i*3 + j
                if min_cost == 0:
                    min_cost = cost
                    print(claw_machine)
                else:
                    min_cost = min(cost, min_cost)
    return min_cost

def parse_lines(lines):

    regex_button = re.compile(r"X\+(\d+).*?Y\+(\d+)")
    regex_prize = re.compile(r"X=(\d+).*?Y=(\d+)")

    lines = lines.splitlines()
    claw_machines = []
    for i in range(0, len(lines), 4):
        
        buttonA_match = regex_button.search(lines[i])
        buttonB_match = regex_button.search(lines[i+1])
        prize_match = regex_prize.search(lines[i+2])
        buttonA = vec2(buttonA_match.group(1), buttonA_match.group(2))
        buttonB = vec2(buttonB_match.group(1), buttonB_match.group(2))
        prize = vec2(prize_match.group(1), prize_match.group(2))

        claw_machine = ClawMachine(buttonA, buttonB, prize)
        claw_machines.append(claw_machine)

    return claw_machines

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    claw_machines = parse_lines(lines)
    res = 0
    for claw_machine in claw_machines:
        res += simulate_claw_reverse(claw_machine)
    print(res)



if __name__ == "__main__":
    main(sys.argv[1:])
