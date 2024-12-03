import re
from itertools import groupby


def read_input(filename):
    with open(filename) as f:
        return [tuple(int(x) for x in re.split(r'\s+', line)[:2]) for line in f.readlines() if line.strip()]
    
    
def part_1(filename):
    lines = read_input(filename)
    left = sorted([x[0] for x in lines])
    right = sorted([x[1] for x in lines])
    distances = [abs(a - b) for a, b in zip(left, right)]
    
    return sum(distances)


def part_2(filename):
    lines = read_input(filename)
    left = sorted([x[0] for x in lines])
    right = sorted([x[1] for x in lines])
    right = {k: len(list(v)) for k, v in groupby(right)}
    
    left = [(x * right.get(x, 0)) for x in left]
    return sum(left)
    
    
def main():
    assert part_1("sample.txt") == 11
    print(f'Solution 1: {part_1("input.txt")}')

    assert part_2("sample.txt") == 31
    print(f'Solution 2: {part_2("input.txt")}')
    
    
if __name__ == "__main__":
    main()