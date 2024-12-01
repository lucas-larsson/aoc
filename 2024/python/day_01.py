from collections import Counter

import numpy as np


def part_one(column_one, column_two) -> int:
    first_array_sorted = np.sort(column_one)
    second_array_sorted = np.sort(column_two)

    total_difference = 0
    for i in range(len(first_array_sorted)):
        total_difference += abs(first_array_sorted[i] - second_array_sorted[i])

    return total_difference

def part_two(column_one, column_two) -> int:
    count_map = Counter(column_two)

    multiplied_results = {num: num * count_map.get(num, 0) for num in column_one}

    return sum(multiplied_results.values())

def read_input(file_path: str) -> np.array:
    with open(file_path, "r") as file:
        first_column = np.array([])
        second_column = np.array([])

        for line in file:
            num1, num2 = map(int, line.split())
            first_column = np.append(first_column, num1)
            second_column = np.append(second_column, num2)

        return first_column, second_column

def day_one():
    file_name = "../input/day_01.txt"
    first_column, second_column = read_input(file_name)

    part_one_solution = part_one(first_column, second_column)
    part_two_solution = part_two(first_column, second_column)

    assert part_one_solution == 1970720
    assert part_two_solution == 17191599

    print(part_one_solution)
    print(part_two_solution)


if __name__ == "__main__":
    day_one()
