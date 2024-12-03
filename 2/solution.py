import re
from dataclasses import dataclass
from typing import List

@dataclass
class Report:
    levels: List[int]


def read_input(filename):
    with open(filename) as f:
        return [Report(levels = [int(x) for x in re.split(r'\s+', line) if x.strip()]) for line in f.readlines() if line.strip()]
    

def is_safe_asc(x, y):
    return 1 <= (y - x) <= 3


def is_safe_desc(x, y):
    return 1 <= (x - y) <= 3

def is_safe(report: Report) -> bool:
    diffs = [(a - b) for a, b in zip(report.levels, report.levels[1:])]
    return (all(x > 0 for x in diffs) or all(x < 0 for x in diffs)) and all(1 <= abs(x) <= 3 for x in diffs)


def is_safe_2(report: Report) -> bool:
    if is_safe(report): return True

    for j in range(1, len(report.levels) - 1):
        if is_safe(Report(levels=[l for i, l in enumerate(report.levels) if i != j]):
            return True)
                
    return False


def part_1(filename):
    reports = read_input(filename)
    return sum(1 for report in reports if is_safe(report))


def part_2(filename):
    reports = read_input(filename)
    return sum(1 for report in reports if is_safe_2(report))


    
def main():
    assert part_1("sample.txt") == 2
    print(f'Solution 1: {part_1("input.txt")}')

    for report in read_input("sample.txt"):
        print(f'{is_safe(report)} {is_safe_2(report)} {report}')
        
    assert part_2("sample.txt") == 4, part_2("sample.txt")
    print(f'Solution 2: {part_2("input.txt")}')
    
    
if __name__ == "__main__":
    main()
    # print(is_safe_2(Report(levels=[1, 3, 2, 4, 5])))
    # part_2("sample.txt")
