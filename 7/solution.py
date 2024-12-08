from typing import List, Tuple, Optional, Set
from itertools import permutations, zip_longest, chain, product
import multiprocessing as mp


def read_input(filename) -> List[Tuple[int, List[int]]]:
    data: List[Tuple[int, List[int]]] = []
    
    with open(filename) as f:
        for line in f.readlines():
            if not line.strip():
                continue
            else:
                left, right = line.split(':')
                data.append((int(left), [int(x) for x in right.split(' ') if x]))

    return data


def valid_ops(required_result: int, operands: List[int], operators: List[str] = ['+', '*']) -> Optional[List[str]]:
    possible_operator_combinations = product(operators, repeat=len(operands) - 1)
    
    for ops in possible_operator_combinations:
        current_result = 0
        
        full_ops = ['='] + list(ops)
        dead_op_prefixes: Set[str] = set()
        
        for operator, operand in zip(full_ops, operands):
            if operator == '=':
                current_result = operand
            elif operator == '+':
                current_result += operand
            elif operator == '*':
                current_result *= operand
            elif operator == '||':
                current_result = int(str(current_result) + str(operand))
            else:
                raise AssertionError(f'Invalid operator {operator}')
            
        if required_result == current_result:
            return full_ops
        elif current_result > required_result:
            continue
         
    return None


def part_1(filename):
    data = read_input(filename)
    return sum(left for left, right in data if valid_ops(left, right))


def part_2(filename):
    data = read_input(filename)
    return sum(left for left, right in data if valid_ops(left, right, ['+', '*', '||']) is not None)


def main():
    assert (value := part_1("sample.txt")) == 3749, f'{value}'
    print(f'Solution 1: {part_1("input.txt")}')
    
    assert (value := part_2("sample.txt")) == 11387, f'{value}'
    print(f'Solution 2: {part_2("input.txt")}')


if __name__ == "__main__":
    main()
