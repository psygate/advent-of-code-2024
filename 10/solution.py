from typing import List, Tuple, Optional, Set, Any, Dict, Union, Iterable, Callable
from itertools import permutations, zip_longest, chain, product, count, repeat
from collections import namedtuple
from pathlib import Path
from os import PathLike
from dataclasses import dataclass
import re


type Position = Tuple[int, int]

@dataclass
class Field:
    values: List[List[Optional[int]]]
    get_starting_points: List[Position]

    @property
    def width(self) -> int:
        return len(self.values[0])
    
    @property
    def height(self) -> int:
        return len(self.values)
    
                    
    def __getitem__(self, index: Position) -> Optional[int]:
        return self.values[index[1]][index[0]]
    
    def __setitem__(self, index: Position, value: Optional[int]):
        self.values[index[1]][index[0]] = value
    
    def __str__(self):
        return '\n'.join([''.join([str(q) if q is not None else '.' for q in l]) for l in self.values])


def read_input(filename: PathLike) -> Field:
    bdata = [[int(q) if q != '.' else None for q in l] for l in Path(filename).read_text().strip().split('\n') if l.strip()]

    starting_points = []
    for y in range(len(bdata)):
        for x in range(len(bdata[y])):
            if bdata[y][x] is not None and bdata[y][x] == 0:
                starting_points.append((x, y))
    
    return Field(bdata, starting_points)
    

def part_1(filename: PathLike):
    field = read_input(filename)
    
    starting_point_peaks: List[Tuple[Tuple[int, int], int]] = []
    
    for starting_point in field.get_starting_points:
        peaks = 0
        visited_nodes = set()
        walk_stack = [starting_point]
        while walk_stack:
            current_x, current_y = walk_stack.pop()
            visited_nodes.add((current_x, current_y))
            for x, y in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                next_x, next_y = current_x + x, current_y + y
                if next_x >= 0 and next_y >= 0 and next_x < field.width and next_y < field.height:
                    
                    assert field[next_x, next_y] is not None 
                    assert field[current_x, current_y] is not None
                     
                    if (field[next_x, next_y] - field[current_x, current_y]) == 1 and (next_x, next_y) not in visited_nodes:
                        if field[next_x, next_y] == 9:
                            peaks += 1
                        
                        walk_stack.append((next_x, next_y))

        starting_point_peaks.append((starting_point, peaks))
        
    return sum([p[1] for p in starting_point_peaks])


    
def part_2(filename: PathLike):
    field = read_input(filename)
    
    starting_point_peaks: List[Tuple[Position, int]] = []
    
    for starting_point in field.get_starting_points:
        peaks = 0
        visited_nodes = set()
        walk_stack = [[starting_point]]
        possible_paths = []
        while walk_stack:
            path = walk_stack.pop()
            current_x, current_y = path[-1]
            
            for x, y in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                next_x, next_y = current_x + x, current_y + y
                if next_x >= 0 and next_y >= 0 and next_x < field.width and next_y < field.height:
                    
                    assert field[next_x, next_y] is not None 
                    assert field[current_x, current_y] is not None
                     
                    if field[next_x, next_y] - field[current_x, current_y] == 1 and (next_x, next_y) not in path:
                        if field[next_x, next_y] == 9:
                            possible_paths.append(list(path) + [(next_x, next_y)])
                            peaks += 1
                        
                        walk_stack.append(list(path) + [(next_x, next_y)])

        starting_point_peaks.append((starting_point, peaks))
        
    return sum([p[1] for p in starting_point_peaks])
    
        

def main():
    assert (value := part_1("sample.txt")) == 36, f'{value}'
    print(f'Solution 1: {part_1("input.txt")}')
    
    assert (value := part_2("sample.txt")) == 81, f'{value}'
    print(f'Solution 2: {part_2("input.txt")}')


if __name__ == "__main__":
    main()
