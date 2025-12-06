def part_one(math_sheet: list) -> int:
    import math

    numbers_and_ops = [line.split() for line in math_sheet]
    operators = numbers_and_ops[-1]
    numbers = numbers_and_ops[:-1]

    results = []
    for c, op in enumerate(operators):
        col = [int(row[c]) for row in numbers]
        if op == "+":
            results.append(sum(col))
        elif op == "*":
            results.append(math.prod(col))

    return sum(results)


def part_two(math_sheet: list) -> int:
    import math

    operator_line = math_sheet[-1]
    operator_positions = [(i, char) for i, char in enumerate(operator_line) if char in '+*']

    numbers = math_sheet[:-1]
    max_line_len = max(len(row) for row in numbers)

    results = []
    for col_start, op in operator_positions:
        next_positions = [pos for pos, _ in operator_positions if pos > col_start]
        col_end = next_positions[0] if next_positions else max_line_len

        col = []
        for row in numbers:
            if len(row) < col_end:
                segment = row[col_start:] + ' ' * (col_end - len(row))
            else:
                segment = row[col_start:col_end]
            col.append(segment)

        new_numbers = []
        for char_pos in range(len(col[0])):
            digits = [segment[char_pos] for segment in col
                     if char_pos < len(segment) and segment[char_pos] != ' ']
            if digits:
                new_numbers.append(int(''.join(digits)))

        new_numbers = new_numbers[::-1]

        if op == "+":
            results.append(sum(new_numbers))
        elif op == "*":
            results.append(math.prod(new_numbers))

    return sum(results)


def day_six():
    file_name = "../input/day_06.txt"
    with open(file_name, 'r') as f:
        math_sheet = f.read().strip().split('\n')

    part_one_solution = part_one(math_sheet)
    part_two_solution = part_two(math_sheet)

    print(f"Part 1: {part_one_solution}")
    print(f"Part 2: {part_two_solution}")


if __name__ == "__main__":
    day_six()
