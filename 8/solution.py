from typing import List, Tuple, Optional, Set, Any, Dict, Union
from itertools import permutations, zip_longest, chain, product, count
from collections import namedtuple
from pathlib import Path
from os import PathLike
from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int
    
    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return self.__class__(self.x * other, self.y * other)
    
    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)
    
    def __lt__(self, other):
        return self.x < other.x and self.y < other.y
    
    def __gt__(self, other):
        return self.x > other.x and self.y > other.y
    
    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y
    
    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y
    
    
    def __hash__(self):
        return hash((self.x, self.y))

type FieldDimensions = Position
type AntennaPositionDict = Dict[str, List[Position]]
type AntinodePositionDict = Dict[str, List[Position]]

IGNORED_ANTENNAS = '.#'

def draw_field(antennas: AntennaPositionDict, antinodes: AntinodePositionDict, field_size: FieldDimensions, ignored_antennas: str = IGNORED_ANTENNAS) -> str:
    field = [['.' for _ in range(field_size.x)] for _ in range(field_size.y)]

    for key, value in antennas.items():
        for pos in value:
            field[pos.y][pos.x] = key

    for key, value in antinodes.items():
        for pos in value:
            if field[pos.y][pos.x] in ignored_antennas:
                field[pos.y][pos.x] = '#'

    return '\n'.join(''.join(row) for row in field)


def read_input(filename: PathLike, ignored_antennas: str = IGNORED_ANTENNAS) -> Tuple[AntennaPositionDict, FieldDimensions]:
    data = [line for line in Path(filename).read_text().strip().split('\n') if line.strip()]
    assert all(len(l) == len(data[0]) for l in data), f'Field is not rectangular {[len(l) for l in data]}'
    
    antennas: AntennaPositionDict = {}
    
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] not in ignored_antennas:
                antennas.setdefault(data[y][x], []).append(Position(x, y))
                
    return antennas, Position(len(data[0]), len(data))


def calculate_antinodes(antennas: AntennaPositionDict, field_size: FieldDimensions) -> AntinodePositionDict:
    antinodes: AntinodePositionDict = {}
    
    for antenna_type, positions in antennas.items():
        for (pos_a, pos_b) in permutations(positions, 2):
            antinode_a_offset = pos_b - pos_a
            antinode_b_offset = pos_a - pos_b
            
            antinode_a = pos_b + antinode_a_offset
            antinode_b = pos_a + antinode_b_offset
            
            if antinode_a >= Position(0, 0) and antinode_a < field_size:
                antinodes.setdefault(antenna_type, []).append(antinode_a)

            if antinode_b >= Position(0, 0) and antinode_b < field_size:
                antinodes.setdefault(antenna_type, []).append(antinode_b)

    return antinodes


def calculate_antinodes_2(antennas: AntennaPositionDict, field_size: FieldDimensions) -> AntinodePositionDict:
    antinodes: AntinodePositionDict = {}
    
    for antenna_type, positions in antennas.items():
        for (pos_a, pos_b) in permutations(positions, 2):
            for position, offset in ((pos_b, pos_b - pos_a), (pos_a, pos_a - pos_b)):
                for direction in (1, -1):
                    for scale in count(1):
                        antinode = position + offset * (scale * direction)
                        
                        if antinode >= Position(0, 0) and antinode < field_size:
                            antinodes.setdefault(antenna_type, []).append(antinode)
                        else:
                            break

    return antinodes


def diff(a: str, b: str):
    return '\n'.join(f'{a_line}\t{b_line}' for a_line, b_line in zip(a.split('\n'), b.split('\n')) if a_line != b_line)


def test(filename: PathLike):
    antennas, field_size = read_input(filename)
    antinodes = calculate_antinodes(antennas, field_size)

    field = draw_field(antennas, antinodes, field_size)
    example = Path(filename).read_text().strip()
    assert field == example, f'{field}\n\n{example}\n\n{diff(field, example)})'


def test_2(filename: PathLike):
    antennas, field_size = read_input(filename)
    antinodes = calculate_antinodes_2(antennas, field_size)

    field = draw_field(antennas, antinodes, field_size)
    example = Path(filename).read_text().strip()
    assert field == example, f'{field}\n\n{example}\n\n{diff(field, example)})'
    

def part_1(filename: PathLike):
    antennas, field_size = read_input(filename)
    antinodes = calculate_antinodes(antennas, field_size)

    return len(set(x for l in antinodes.values() for x in l))


def part_2(filename: PathLike):
    antennas, field_size = read_input(filename)
    antinodes = calculate_antinodes_2(antennas, field_size)

    return len(set(x for l in antinodes.values() for x in l))




def main():
    test("sample_2.txt")
    test("sample_3.txt")
    assert (value := part_1("sample.txt")) == 14, f'{value}'
    print(f'Solution 1: {part_1("input.txt")}')
    
    test_2("sample_4.txt")
    test_2("sample_5.txt")
    
    assert (value := part_2("sample.txt")) == 34, f'{value}'
    print(f'Solution 2: {part_2("input.txt")}')


if __name__ == "__main__":
    main()
