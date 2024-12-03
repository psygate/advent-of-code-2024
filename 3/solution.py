import re

MUL_INSTR = re.compile('(?P<opmul>mul)\((\d+),(\d+)\)')
DO_INSTR = re.compile('(?P<opdo>do)\(\)')
DONT_INSTR = re.compile("(?P<opdont>don't)\(\)")

INSTRUCTION_PATTERN  =  re.compile(MUL_INSTR.pattern + '|' + DO_INSTR.pattern + '|' + DONT_INSTR.pattern)

def read_input(filename):
    with open(filename) as f:
        return f.read()

    
def part_1(filename):
    instr = read_input(filename)
    
    value = 0
    for mul_inst in MUL_INSTR.finditer(instr):
        value += int(mul_inst.group(2)) * int(mul_inst.group(3))
    
    return value

def part_2(filename):
    instructions = read_input(filename)
    
    value = 0
    enabled = True
    for instr in INSTRUCTION_PATTERN.finditer(instructions):
        if instr.group('opmul'):
            if enabled:
                value += int(instr.group(2)) * int(instr.group(3))
        elif instr.group('opdo'):
            enabled = True
        elif instr.group('opdont'):
            enabled = False
            
    
    return value
        

def main():
    assert part_1("sample.txt") == 161
    print(f'Solution 1: {part_1("input.txt")}')

    assert part_2("sample_2.txt") == 48
    print(f'Solution 2: {part_2("input.txt")}')
    
if __name__ == "__main__":
    main()

