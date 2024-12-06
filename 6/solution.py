import re
from typing import List, Tuple
from enum import StrEnum
from  collections import namedtuple

class Field(StrEnum):
    FREE = '.'
    OBSTACLE = '#'
    VISITED = 'X'


class Guard(StrEnum):
    UP = '^'
    LEFT = '<'
    RIGHT = '>'
    DOWN = 'v'


GuardPosition = namedtuple('GuardPosition', ['x', 'y'])
movement_map = {Guard.UP: (0, -1), Guard.LEFT:  (-1,  0), Guard.RIGHT: (1, 0), Guard.DOWN: (0, 1)}
movement_update_turn_right_map = {Guard.UP: Guard.RIGHT, Guard.LEFT: Guard.UP, Guard.RIGHT: Guard.DOWN, Guard.DOWN: Guard.LEFT}


def read_input(filename):
    with open(filename) as f:
        return [[i for i in l.strip()] for l in f.readlines() if l.strip()]


def find_guard(field: List[str]) -> GuardPosition:
    assert all(len(field[0]) == len(row) for row in field), 'Field is not rectangular'
    
    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] in [Guard.UP, Guard.LEFT, Guard.RIGHT, Guard.DOWN]:
                return GuardPosition(x,  y)

    raise ValueError('Guard not found')
    
    
def in_field(guard_pos,  field):
    return 0 <= guard_pos.x < len(field) and 0 <= guard_pos.y < len(field[0])
    

def turn_right(guard_state: Guard) -> Guard:
    return movement_update_turn_right_map[guard_state]
      

def part_1(filename):
    field = read_input(filename)
    guard_pos = find_guard(field)
    assert field[guard_pos.y][guard_pos.x] in movement_map, f'Invalid guard position. {guard_pos} {field[guard_pos.y][guard_pos.x]}'
    
    while True:
        guard_state = field[guard_pos.y][guard_pos.x]
        movement = movement_map[guard_state]
        next_pos = GuardPosition(guard_pos.x + movement[0], guard_pos.y + movement[1])
        
        if not in_field(next_pos,  field):
            field[guard_pos.y][guard_pos.x] = Field.VISITED
            break

        field_value = field[next_pos.y][next_pos.x]
        
        if field_value == Field.FREE or field_value == Field.VISITED:
            field[guard_pos.y][guard_pos.x] = Field.VISITED
            field[next_pos.y][next_pos.x] = guard_state
            guard_pos = next_pos
        elif field_value == Field.OBSTACLE:
            field[guard_pos.y][guard_pos.x] = turn_right(guard_state)
        else:
            raise ValueError(f'Invalid movement. {guard_state} {movement} {guard_pos} {next_pos} {field_value}')
    
    return sum(1 for row in field for cell in row if cell == Field.VISITED)

def part_2(filename):
    pass
    

def main():
    assert part_1("sample.txt") == 41, f'{part_1("sample.txt")}'
    print(f'Solution 1: {part_1("input.txt")}')
    
    # assert part_2("sample.txt") == 123, f'{part_2("sample.txt")}'
    # print(f'Solution 2: {part_2("input.txt")}')


if __name__ == "__main__":
    main()
