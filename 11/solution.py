from typing import List, Tuple, Optional, Set, Any, Dict, Union, Iterable, Callable
from itertools import permutations, zip_longest, chain, product, count, repeat
from collections import namedtuple
from pathlib import Path
from os import PathLike
from dataclasses import dataclass
import re
import multiprocessing as mp
from functools import lru_cache

def read_input(filename: PathLike) -> List[int]:
    bdata = [int(y) for l in Path(filename).read_text().strip().split('\n') for y in re.findall(r'\d+', l) if l.strip()]

    return bdata


@lru_cache(maxsize=None)
def blink(num: int, iteration_num: int) -> List[int]:
    assert iteration_num >= 0
    if iteration_num == 0:
        return [num]
    
    if num == 0:
        return blink(1, iteration_num - 1)
    
    numstr = str(num)
    numlen = len(numstr)
    if numlen & 1 == 0:
        left, right = int(numstr[:numlen // 2]), int(numstr[numlen // 2:])
        return blink(left, iteration_num - 1) + blink(right, iteration_num - 1)
    else:
        return blink(num * 2024, iteration_num - 1)


@lru_cache(maxsize=None)
def blink_len(num: int, iteration_num: int):
    if iteration_num == 0:
        return 1

    if num == 0:
        return blink_len(1, iteration_num - 1)

    numstr = str(num)
    numlen = len(numstr)

    if (numlen & 1) == 0:
        return blink_len(int(numstr[:numlen // 2]), iteration_num - 1) + blink_len(int(numstr[numlen // 2:]), iteration_num - 1)

    return blink_len(num * 2024, iteration_num - 1)

    
    
def part_1(filename: PathLike):
    data = read_input(filename)
    
    return len([y for x in data for y in blink(x, 25)])


    
def part_2(filename: PathLike):
    data = read_input(filename)
    
    return sum(blink_len(x, 75) for x in data)

    
def main():
    assert (value := [y for x in [0, 1, 10, 99, 999] for y in blink(x, 1)]) == [1, 2024, 1, 0, 9, 9, 2021976], f'{value}'
    assert (value := [y for x in [125, 17] for y in blink(x, 1)]) == [253000, 1, 7], f'{value}'
    assert (value := [y for x in [125, 17] for y in blink(x, 2)]) == [253, 0, 2024, 14168], f'{value}'
    assert (value := [y for x in [125, 17] for y in blink(x, 3)]) == [512072, 1, 20, 24, 28676032], f'{value}'
    assert (value := [y for x in [125, 17] for y in blink(x, 4)]) == [512, 72, 2024, 2, 0, 2, 4, 2867, 6032], f'{value}'
    assert (value := [y for x in [125, 17] for y in blink(x, 5)]) == [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32], f'{value}'
    assert (value := [y for x in [125, 17] for y in blink(x, 6)]) == [2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2], f'{value}'
    
    assert (value := part_1("sample.txt")) == 55312, f'{value}'
    assert (value := part_1("input.txt")) == 203953, f'{value}'
    print(f'Solution 1: {part_1("input.txt")}')
    
    print(f'Solution 2: {part_2("input.txt")}')


if __name__ == "__main__":
    main()
