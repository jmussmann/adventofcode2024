import sys
import os
from copy import deepcopy

class Vec2:

    def __init__(self, x, y):

        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        raise NotImplementedError

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        raise NotImplementedError

    def __mul__(self, other):

        if isinstance(other, int) or isinstance(other, float):
            return Vec2(self.x * other, self.y * other)
        if  isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        raise NotImplementedError

    __rmul__ = __mul__

    def __div__(self, other):

        if isinstance(other, int) or isinstance(other, float):
            return Vec2(self.x / other, self.y / other)
        raise NotImplementedError

    def __str__(self):

        return f"vec2({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, Vec2):
            raise NotImplementedError

        if self.x == other.x and self.y == other.y:
            return True
        
        return False

class Box:

    def __init__(self, pos):

        self.start = Vec2(pos.x*2, pos.y)
        self.end = self.start+Vec2(1, 0)
    
    def get_gps(self):

        return (self.start.y+1)*100 + self.end.x + 1

class Warehouse:

    def __init__(self, warehouse_map):
        self.dim_x = (len(warehouse_map[0]) - 2)*2
        self.dim_y = len(warehouse_map) - 2

        self.boxes = []
        self.walls = {}
        self.initial_robot_pos = Vec2(0,0)
        for i in range(1, len(warehouse_map)-1):
            y = i - 1
            for j in range(1, len(warehouse_map[i])-1):
                x = j-1
                el = warehouse_map[i][j]
                pos = Vec2(x, y)
                if el == "#":
                    wall_pos = Vec2(pos.x*2, pos.y)
                    self.walls[wall_pos] = True
                    self.walls[wall_pos+Vec2(1, 0)] = True
                elif el == "O":
                    self.boxes.append(Box(pos))
                elif el == "@":
                    self.initial_robot_pos = Vec2(pos.x*2, pos.y)
                    
    def print(self, robot=None):

        to_print_top_bot = ["#"]
        for x in range(0, self.dim_x+1):
            to_print_top_bot.append("#")

        print("".join(to_print_top_bot))

        for y in range(0, self.dim_y):
            to_print = ["#"]
            for x in range(0, self.dim_x):
                pos = Vec2(x, y)
                if self.pos_has_wall(pos):
                    to_print.append("#")
                elif self.pos_has_box_left(pos):
                    to_print.append("[")
                elif self.pos_has_box_right(pos):
                    to_print.append("]")
                elif robot is not None and robot.pos == pos:
                    to_print.append("@")
                else:
                    to_print.append(".")
            to_print.append("#")
            print("".join(to_print))
        print("".join(to_print_top_bot))

    def get_checksum(self):

        res = 0
        for box in self.boxes:
            res += box.get_gps()
        return res


    def pos_has_wall(self, pos):
        if pos in self.walls or pos.x < 0 or pos.x >= self.dim_x or pos.y < 0 or pos.y >= self.dim_y:
            return True
        return False
    def pos_has_box(self, pos):
        for box in self.boxes:
            if pos.y == box.start.y and (pos.x == box.start.x or pos.x == box.end.x):
                return True
        return False
    def pos_has_box_right(self, pos):
        for box in self.boxes:
            if pos.y == box.start.y and pos.x == box.end.x:
                return True
        return False
    def pos_has_box_left(self, pos):
        for box in self.boxes:
            if pos.y == box.start.y and pos.x == box.start.x:
                return True
        return False
    def get_box(self, pos):
        for idx, box in enumerate(self.boxes):
            if (pos.y == box.start.y and pos.x == box.start.x) or (pos.y == box.end.y and pos.x == box.end.x):
                return box, idx
        return None, -1
    def pos_is_empty(self, pos):

        if pos.x > -1 and pos.x < self.dim_x and pos.y > -1 and pos.y < self.dim_y and not self.pos_has_wall(pos) and not self.pos_has_box(pos):
            return True
        return False

class Robot:

    def __init__(self, pos, program):

        self.pos = pos
        self.program = program
        self.pc = 0


    def do_update(self, move, pos, warehouse):
        updates = []
        to_update = []
        box, _ = warehouse.get_box(pos)
        do_update = False
        new_pos = Vec2(0,0)
        if move == Vec2(1, 0):
            new_pos = box.end + move
            if warehouse.pos_has_wall(box.end + move):
                return False, []
            elif warehouse.pos_has_box(box.end + move): 
                do_update, to_update = self.do_update(move, box.end + move, warehouse) 
            else:
                do_update = True
        elif move == Vec2(-1, 0):
            new_pos = box.start + move
            if warehouse.pos_has_wall(box.start + move):
                return False, []
            elif warehouse.pos_has_box(box.start + move): 
                do_update, to_update = self.do_update(move, box.start + move, warehouse) 
            else:
                do_update = True
        elif move == Vec2(0, -1) or move == Vec2(0, 1):
            new_pos = box.start + move
            if warehouse.pos_has_wall(box.start + move) or warehouse.pos_has_wall(box.end + move):
                return False, []
            elif warehouse.pos_has_box(box.start + move) or warehouse.pos_has_box(box.end + move):
                do_update1 = True
                do_update2 = True
                to_update1 = []
                to_update2 = []
                box1, _ = warehouse.get_box(box.start + move)
                box2, _ = warehouse.get_box(box.end + move)
                if warehouse.pos_has_box(box.start + move):
                    do_update1, to_update1 = self.do_update(move, box.start + move, warehouse)
                if warehouse.pos_has_box(box.end + move) and (box1 is None or not box1.start == box2.start):
                    do_update2, to_update2 = self.do_update(move, box.end + move, warehouse)
                do_update = (do_update1 and do_update2)
                to_update = to_update1 + to_update2
                #print(to_update)
            else:
                do_update = True
        #if new_pos == Vec2(11,75):
        #    print(updates)
        #    raise

        if do_update:
            updates += to_update
            if move == Vec2(1, 0):
                new_pos_end = new_pos
                new_pos_start = new_pos + Vec2(-1, 0) 
            elif move == Vec2(-1, 0):
                new_pos_start = new_pos
                new_pos_end = new_pos + Vec2(1, 0)
            elif move == Vec2(0, -1) or move == Vec2(0, 1):
                new_pos_start = new_pos
                new_pos_end = new_pos + Vec2(1, 0) 
            updates += [[pos, new_pos_start, new_pos_end]]

            return True, updates

        return False, []

    def apply_update(self, updates, warehouse):
        new_boxes = deepcopy(warehouse.boxes)
        for update in updates:
            box, idx = warehouse.get_box(update[0])
            if box is None:
                print(update[0])
            new_boxes[idx].start = update[1]
            new_boxes[idx].end = update[2]
        
        warehouse.boxes = new_boxes

    def run_program(self, warehouse):
        for pc in range(self.pc, len(self.program)):
            self.pc = pc
            
            if pc % 10 == 0 and len(self.program) > self.pc+1:
                print(f"{pc}/{len(self.program)}")
                #print(f"Program: {self.pc} -> ",repr(self.program[self.pc]), repr(self.program[self.pc+1]))
            
            move = self.get_move()
            new_pos = self.pos + move
    
            if warehouse.pos_has_wall(new_pos):
                continue
            elif warehouse.pos_is_empty(new_pos):
                self.pos = new_pos
                #print(new_pos)
            else:
                box, _ = warehouse.get_box(self.pos+move)
                do_update, updates = self.do_update(move, box.start, warehouse)
                #print(updates)
                if do_update:
                    self.apply_update(updates, warehouse)
                    self.pos = new_pos
            
            #if pc > 1 or True:
            #    warehouse.print(self)
            #    input()


    def get_move(self):

        el = self.program[self.pc]
        #print(f"Move: {el}, Pos: {self.pos}")
        if el == "<":
            return Vec2(-1, 0)
        if el == ">":
            return Vec2(1, 0)
        if el == "^":
            return Vec2(0, -1)
        if el == "v":
            return Vec2(0, 1)

        return Vec2(0, 0)



def parse_lines(lines):

    warehouse_lines, program_lines = lines.split("\n\n")
    
    warehouse_map = []
    for line in warehouse_lines.splitlines():
        warehouse_map.append(list(line))
    warehouse = Warehouse(warehouse_map)
    robot = Robot(warehouse.initial_robot_pos, list(program_lines.strip().replace("\n", "")))
    #warehouse.print(robot)
        
    return warehouse, robot

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    warehouse, robot = parse_lines(lines)

    warehouse.print(robot)
    input()
    robot.run_program(warehouse)
    warehouse.print(robot)

    print("Res: ", warehouse.get_checksum())



if __name__ == "__main__":
    main(sys.argv[1:])
