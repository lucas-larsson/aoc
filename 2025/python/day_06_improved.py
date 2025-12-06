import math
from typing import List


def part_one(math_sheet: List[str]) -> int:
    """
    Part 1: Read problems vertically as columns.
    Each column is a separate problem with numbers stacked vertically.
    """
    rows = [line.split() for line in math_sheet]
    operators = rows[-1]
    numbers = rows[:-1]

    results = []
    for col_idx, op in enumerate(operators):
        column_values = [int(row[col_idx]) for row in numbers]

        if op == "+":
            results.append(sum(column_values))
        else:  # op == "*"
            results.append(math.prod(column_values))

    return sum(results)


def part_two(math_sheet: List[str]) -> int:
    """
    Part 2: Read cephalopod math (right-to-left in columns).
    Each number is written vertically with most significant digit at top.
    Spaces in the input preserve alignment.
    """
    operator_line = math_sheet[-1]
    number_lines = math_sheet[:-1]

    # Find where each problem starts (operator positions)
    operators = [(i, char) for i, char in enumerate(operator_line) if char in '+*']

    results = []
    for idx, (col_start, op) in enumerate(operators):
        # Determine column boundaries
        col_end = operators[idx + 1][0] if idx + 1 < len(operators) else max(len(line) for line in number_lines)

        # Extract the character segment for this problem from each row
        segments = [line[col_start:col_end].ljust(col_end - col_start) for line in number_lines]

        # Read vertically through each character position (left to right)
        # This forms numbers by reading digits top-to-bottom at each position
        numbers = []
        for char_pos in range(col_end - col_start):
            digits = [seg[char_pos] for seg in segments if seg[char_pos] != ' ']
            if digits:
                numbers.append(int(''.join(digits)))

        # Reverse for right-to-left processing (rightmost column = least significant)
        numbers.reverse()

        # Apply operator
        result = sum(numbers) if op == "+" else math.prod(numbers)
        results.append(result)

    return sum(results)


def part_one_functional(math_sheet: List[str]) -> int:
    """Alternative: More functional/compact approach for Part 1"""
    rows = [line.split() for line in math_sheet]
    ops = rows[-1]
    nums = rows[:-1]

    return sum(
        sum(int(row[i]) for row in nums) if op == "+" else math.prod(int(row[i]) for row in nums)
        for i, op in enumerate(ops)
    )


def extract_problem_column(lines: List[str], start: int, end: int) -> List[str]:
    """Helper: Extract and normalize a problem column from the input."""
    width = end - start
    return [line[start:end].ljust(width) for line in lines]


def read_vertical_numbers(segments: List[str]) -> List[int]:
    """Helper: Read numbers by going vertically through character positions."""
    if not segments:
        return []

    numbers = []
    for char_pos in range(len(segments[0])):
        digits = [seg[char_pos] for seg in segments if char_pos < len(seg) and seg[char_pos] != ' ']
        if digits:
            numbers.append(int(''.join(digits)))

    return numbers


def part_two_refactored(math_sheet: List[str]) -> int:
    """Alternative: Part 2 with helper functions for clarity"""
    operator_line = math_sheet[-1]
    number_lines = math_sheet[:-1]
    max_len = max(len(line) for line in number_lines)

    operators = [(i, char) for i, char in enumerate(operator_line) if char in '+*']

    results = []
    for idx, (start, op) in enumerate(operators):
        end = operators[idx + 1][0] if idx + 1 < len(operators) else max_len

        segments = extract_problem_column(number_lines, start, end)
        numbers = read_vertical_numbers(segments)
        numbers.reverse()  # Right-to-left processing

        result = sum(numbers) if op == "+" else math.prod(numbers)
        results.append(result)

    return sum(results)


def day_six():
    file_name = "../input/day_06.txt"
    with open(file_name, 'r') as f:
        math_sheet = f.read().strip().split('\n')

    print(f"Part 1 (original):    {part_one(math_sheet)}")
    print(f"Part 1 (functional):  {part_one_functional(math_sheet)}")
    print(f"Part 2 (improved):    {part_two(math_sheet)}")
    print(f"Part 2 (refactored):  {part_two_refactored(math_sheet)}")


if __name__ == "__main__":
    day_six()