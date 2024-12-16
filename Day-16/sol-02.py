import sys
import os
from copy import deepcopy
import multiprocessing

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

    def dot(self, other):

        if not isinstance(other, Vec2):
            raise NotImplementedError

        return self.x * other.x + self.y * other.y

class Field:

    def __init__(self, start, end, dim_x, dim_y, walls):
        self.dim_x = dim_x
        self.dim_y = dim_y

        self.start = start
        self.end = end
        self.walls = walls

        self.bests = {}
        
                    
    def print(self, reindeer=None):

        to_print_top_bot = ["#"]
        for x in range(0, self.dim_x+1):
            to_print_top_bot.append("#")

        print("".join(to_print_top_bot))

        for y in range(0, self.dim_y):
            to_print = ["#"]
            for x in range(0, self.dim_x):
                pos = Vec2(x, y)
                if reindeer is not None and pos == reindeer.pos: 
                    to_print.append("R")
                elif pos == self.start:
                    to_print.append("S")
                elif pos == self.end:
                    to_print.append("E")
                elif pos in self.walls: 
                    to_print.append("#")
                else:
                    to_print.append(".")
            to_print.append("#")
            print("".join(to_print))
        print("".join(to_print_top_bot))

    def is_free(self, pos):
        if (pos.x > -1 and pos.y > -1 and pos.x < self.dim_x and pos.y < self.dim_y and
            pos not in self.walls):
                return True
        return False



class Reindeer:

    def __init__(self, start, score = 0, visited = {}):

        self.pos = start
        self.visited = visited
        self.score = score
        self.finished = False
        self.cancled = False
        self.move = Vec2(1, 0)

    def get_next_reindeer(self, field):

        next_reindeers = []

        for move in [Vec2(-1, 0), Vec2(1, 0), Vec2(0, -1), Vec2(0, 1)]:
            new_pos = self.pos+move
            if field.is_free(new_pos) and new_pos not in self.visited:
                new_reindeer = Reindeer(new_pos, deepcopy(self.score), deepcopy(self.visited))
                new_reindeer.move = move
                new_reindeer.visited[self.pos] = True

                dot = self.move.dot(move)
                if dot == -1:
                    new_reindeer.score += 2000
                elif dot == 0:
                    new_reindeer.score += 1000
                new_reindeer.score += 1
                if new_reindeer.pos in field.bests:
                    if new_reindeer.move in field.bests[new_reindeer.pos]:
                        if new_reindeer.score > field.bests[new_reindeer.pos][move]:
                            continue
                

                if new_reindeer.pos not in field.bests:
                    field.bests[new_reindeer.pos] = {}

                field.bests[new_reindeer.pos][move] = new_reindeer.score

                if new_reindeer.pos == field.end:
                    new_reindeer.finished = True
                next_reindeers.append(new_reindeer)


        return next_reindeers

    def __str__(self):

        return f"Reindeer(Pos: {self.pos}, Score: {self.score})"

    def __repr__(self):
        return str(self)

def parse_lines(lines):

    lines = lines.splitlines()
    y_dim = len(lines)-2
    x_dim = len(lines[1])-2
    start = Vec2(0,0)
    end = Vec2(0,0)
    wall_map = {}

    for i in range (1, len(lines)-1):
        y = i - 1
        for j in range(1, len(lines[i])-1):
            x = j - 1
            el = lines[i][j]
            if el == "S":
                start = Vec2(x, y)
            elif el == "E":
                end = Vec2(x, y)
            elif el == "#":
                wall_map[Vec2(x, y)] = Vec2(x, y)

    field = Field(start, end, x_dim, y_dim, wall_map)

    return field

def process_raindeer(tarsk):
    pass

    

def play(field):

    reindeers = [Reindeer(field.start)]
    finished_reindeers = []

    i = 0
    #with multiprocessing.Pool() as pool:
    while len(reindeers) > 0:
        #if i % 100 == 0:
        print(f"Current queue:" , len(reindeers), f"Iteration {i}", f"Finished: {len(finished_reindeers)}")
        i += 1
        new_reindeers = []
        #for new_eindeers in pool.map(process_raindeer, old_line):
        for reindeer in reindeers:
            if reindeer.finished:
                finished_reindeers.append(reindeer)
                continue
            if reindeer.cancled:
                continue
            new_reindeers += reindeer.get_next_reindeer(field)

        reindeers = new_reindeers

    print(finished_reindeers)

    min_score = finished_reindeers[0].score
    for reindeer in finished_reindeers:
        min_score = min(min_score, reindeer.score)

    min_reindeers = []
    for reindeer in finished_reindeers:
        if min_score == reindeer.score:
            min_reindeers.append(reindeer)
    visited_map = {}
    for reindeer in min_reindeers:
        for el in reindeer.visited.keys():
            visited_map[el] = True
        
    print("Res2:", len(visited_map.keys())+1)

    return min_score

def main(argv):

    with open(argv[0], "r") as fd:
        lines = fd.read()

    field = parse_lines(lines)

    field.print()

    print("Res: ", play(field))



if __name__ == "__main__":
    main(sys.argv[1:])
