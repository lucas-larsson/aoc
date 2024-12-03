import re

file_name = "../input/day_03.txt"


def read_input(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read().strip()

def extract_instructions(pattern) -> list:
    return re.findall(pattern, read_input(file_name))

def part_one() -> int:
    multiplication_pattern = r"mul\((\d+),(\d+)\)"
    extracted_inst = extract_instructions(multiplication_pattern)
    total_sum = 0
    for x, y in extracted_inst:
        total_sum += int(x) * int(y)
    return total_sum

def part_two():
    conditional_multiplication_pattern = r"(do\(\)|don't\(\)|mul\(\d+,\d+\))"
    extracted_inst = extract_instructions(conditional_multiplication_pattern)

    mul_enabled = True  # Initially, mul instructions are enabled
    total_sum = 0

    for instruction in extracted_inst:
        if instruction == "do()":
            mul_enabled = True
        elif instruction == "don't()":
            mul_enabled = False
        elif instruction.startswith("mul(") and mul_enabled:
            match = re.match(r"mul\((\d+),(\d+)\)", instruction)
            if match:
                x, y = map(int, match.groups())
                total_sum += x * y

    return total_sum


def day_one():
    part_one_solution = part_one()
    part_two_solution = part_two()

    assert part_one_solution == 183669043
    assert part_two_solution == 59097164

    print(part_one_solution)
    print(part_two_solution)

if __name__ == "__main__":
    day_one()
