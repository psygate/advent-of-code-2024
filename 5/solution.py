import re
from typing import List
from dataclasses import dataclass

def read_input(filename):
    updates = []
    page_ordering_rules = []
    
    with open(filename) as f:
        for line in f.readlines():
            if line.strip():
                matcher = re.match(r'^(\d+)\|(\d+)$', line)
                if matcher:
                    page_ordering_rules.append((int(matcher.group(1)), int(matcher.group(2))))
                    continue
                             
                matcher = re.match(r'^(?:(\d+),)*(\d+)$', line)
                if matcher:
                    updates.append([int(x) for x in line.split(',')])
                    continue
                    
                
    return updates, page_ordering_rules


def is_valid_ordering(update, page_ordering_rules):
    for before_idx in range(len(update)):
        for after_idx in  range(before_idx + 1, len(update)):
            if (update[after_idx], update[before_idx]) in page_ordering_rules:
                return False
    
    return True


def reorder(update, page_ordering_rules):
    for before_idx in range(len(update)):
        for after_idx in  range(before_idx + 1, len(update)):
            if (update[after_idx], update[before_idx]) in page_ordering_rules:
                #swap list elements
                before, after = update[before_idx], update[after_idx]
                update[before_idx] = after
                update[after_idx] = before
                return reorder(update, page_ordering_rules)
    
    return update


def part_1(filename):
    updates, page_ordering_rules = read_input(filename)

    valid_updates = [update for update in updates if is_valid_ordering(update, page_ordering_rules)]
    assert all(len(x) % 2 == 1 for x in valid_updates)
    
    return sum(x[(len(x) - 1) // 2] for x in valid_updates)
    

def part_2(filename):
    updates, page_ordering_rules = read_input(filename)

    invalid_updates = [reorder(update,  page_ordering_rules) for update in updates if not is_valid_ordering(update, page_ordering_rules)]
    assert all(len(x) % 2 == 1 for x in invalid_updates)
    
    
    return sum(x[(len(x) - 1) // 2] for x in invalid_updates)
    

def main():
    assert part_1("sample.txt") == 143, f'{part_1("sample.txt")}'
    print(f'Solution 1: {part_1("input.txt")}')
    
    assert part_2("sample.txt") == 123, f'{part_2("sample.txt")}'
    print(f'Solution 2: {part_2("input.txt")}')


if __name__ == "__main__":
    main()
