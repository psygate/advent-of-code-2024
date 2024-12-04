import re
from typing import List


def read_input(filename):
    with open(filename) as f:
        return [l.strip() for l in f.readlines() if l.strip()]


def rot90(data: List[str]) -> List[str]:
    assert all(len(data[0]) == len(line) for line in data)
    
    output = []
    for i in range(len(data[0])):
        output.append(''.join([line[i] for line in data]))
    
    return output[::-1]

def rot180(data: List[str]) -> List[str]:
    return rot90(rot90(data))


def rot270(data: List[str]) -> List[str]:
    return rot90(rot90(rot90(data)))


def get_diagonals(data: List[str]):
    diagonals: List[List[str]] = [[]]
    
    for x in range(len(data[0])):
        y = 0
        while x < len(data[0]) and y < len(data):
            diagonals[-1].append(data[y][x])
            x += 1
            y += 1
        diagonals.append([])
    
    for y in range(1, len(data)):
        x = 0
        while x < len(data[0]) and y < len(data):
            diagonals[-1].append(data[y][x])
            x += 1
            y += 1
        diagonals.append([])
        
    return [''.join(x) for x in diagonals[:-1]]


def part_1(filename):
    data  = read_input(filename)
    assert all(len(data[0]) == len(line) for line in data)

    count = 0
    basedata = [data, rot90(data), rot180(data), rot270(data), get_diagonals(data), get_diagonals(rot90(data)), get_diagonals(rot180(data)), get_diagonals(rot270(data))]
    
    assert (lenA := len(basedata)) == (lenB := len(set(['\n'.join(x) for x in basedata]))), f'{lenA} != {lenB}'

    for rotated_data in basedata:
        for line in rotated_data:
            if not isinstance(line, str): line = ''.join(line)
            count += len(re.findall(r'XMAS', line))

    return count


def is_diag_xmas(data: List[str], x: int, y: int) -> bool:
    offsets_A =  (-1, -1), (0, 0), (1, 1)
    offsets_B =  (1, -1), (0, 0), (-1, 1)
    
    valueA  = ''.join([data[y + yoff][x + xoff] for xoff, yoff in offsets_A])
    valueB = ''.join([data[y + yoff][x + xoff] for xoff, yoff in offsets_B])
    
    return (valueA == 'MAS'  or valueA == 'SAM') and (valueB == 'MAS' or valueB == 'SAM')


def is_cross_xmas(data: List[str], x: int, y: int) -> bool:
    offsets_A =  (-1, 0), (0, 0), (1, 0)
    offsets_B =  (0, -1), (0, 0), (0, 1)
 
    valueA  = ''.join([data[y + yoff][x + xoff] for xoff, yoff in offsets_A])
    valueB = ''.join([data[y + yoff][x + xoff] for xoff, yoff in offsets_B])
    
    return (valueA == 'MAS'  or valueA == 'SAM') and (valueB == 'MAS' or valueB == 'SAM')


def flip(data: List[str]) -> List[str]:
    return [line[::-1] for line in data[::-1]]


def part_2(filename):
    data  = read_input(filename)

    count = 0

    for x in range(1, len(data[0]) - 1):
        for y in range(1, len(data) - 1):
            if is_diag_xmas(data, x, y):
                count += 1


    return count
        

def main():
    assert part_1("sample.txt") == 18, f'{part_1("sample.txt")}'
    print(f'Solution 1: {part_1("input.txt")}')
    
    assert part_2("sample_2.txt") == 9, f'{part_2("sample_2.txt")}'
    print(f'Solution 2: {part_2("input.txt")}')

if __name__ == "__main__":
    main()
