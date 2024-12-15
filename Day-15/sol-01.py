import sys

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

        self.pos = pos
    
    def get_gps(self):

        return (self.pos.y+1)*100 + self.pos.x + 1

class Warehouse:

    def __init__(self, warehouse_map):
        self.dim_x = len(warehouse_map[0]) -2
        self.dim_y = len(warehouse_map) - 2

        self.boxes = {}
        self.walls = {}
        self.initial_robot_pos = Vec2(0,0)
        for i in range(1, len(warehouse_map)-1):
            y = i - 1
            for j in range(1, len(warehouse_map[i])-1):
                x = j-1
                el = warehouse_map[i][j]
                pos = Vec2(x, y)
                if el == "#":
                    self.walls[pos] = True
                elif el == "O":
                    self.boxes[pos] = Box(pos)
                elif el == "@":
                    self.initial_robot_pos = pos
                    
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
                elif self.pos_has_box(pos):
                    to_print.append("O")
                elif robot is not None and robot.pos == pos:
                    to_print.append("@")
                else:
                    to_print.append(".")
            to_print.append("#")
            print("".join(to_print))
        print("".join(to_print_top_bot))

    def get_checksum(self):

        res = 0
        for box in self.boxes.values():
            res += box.get_gps()
        return res


    def pos_has_wall(self, pos):
        if pos in self.walls or pos.x < 0 or pos.x >= self.dim_x or pos.y < 0 or pos.y >= self.dim_y:
            return True
        return False
    def pos_has_box(self, pos):
        if pos in self.boxes:
            return True
        return False
    def pos_is_empty(self, pos):

        if pos.x > -1 and pos.x < self.dim_x and pos.y > -1 and pos.y < self.dim_y and not self.pos_has_wall(pos) and not self.pos_has_box(pos):
            return True
        return False

class Robot:

    def __init__(self, pos, program):

        self.pos = pos
        self.program = program
        self.pc = 0

    def run_program(self, warehouse):

        for pc in range(self.pc, len(self.program)):
            self.pc = pc
            
            move = self.get_move()
            new_pos = self.pos + move
    
            if warehouse.pos_has_wall(new_pos):
                continue
            update_positions = [new_pos]
            #print(update_positions[-1])
            while warehouse.pos_has_box(update_positions[-1]):
                update_positions.append(update_positions[-1] + move)
                #print(update_positions, move)

            #print(update_positions, warehouse.pos_is_empty(update_positions[-1]))
            if warehouse.pos_is_empty(update_positions[-1]):
                for i in range(len(update_positions)-1, 0, -1):
                    box = warehouse.boxes.pop(update_positions[i-1])
                    box.pos = update_positions[i]
                    warehouse.boxes[update_positions[i]] = box
                self.pos = new_pos
            #print(self.pos)
            #warehouse.print(self)



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
    robot = Robot(warehouse.initial_robot_pos, list(program_lines.strip()))
    #warehouse.print(robot)
        
    return warehouse, robot

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    warehouse, robot = parse_lines(lines)

    robot.run_program(warehouse)
    warehouse.print()

    print("Res: ", warehouse.get_checksum())



if __name__ == "__main__":
    main(sys.argv[1:])
