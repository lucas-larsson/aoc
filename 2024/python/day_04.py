import re
from typing import List, Any

import numpy as np
from numpy import ndarray, dtype

file_name = "../input/day_04.txt"

def count_word_in_matrix(matrix, word):
    word_length = len(word)
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    count = 0

    # Helper function to check a word in a specific direction
    def matches_direction(r, c, dr, dc):
        for i in range(word_length):
            nr, nc = r + i * dr, c + i * dc
            if not (0 <= nr < num_rows and 0 <= nc < num_cols) or matrix[nr][nc] != word[i]:
                return False
        return True

    # Scan all directions
    directions = [
        (0, 1),  # Horizontal right
        (0, -1), # Horizontal left
        (1, 0),  # Vertical down
        (-1, 0), # Vertical up
        (1, 1),  # Diagonal forward down
        (-1, -1),# Diagonal forward up
        (1, -1), # Diagonal backward down
        (-1, 1), # Diagonal backward up
    ]

    for r in range(num_rows):
        for c in range(num_cols):
            for dr, dc in directions:
                if matches_direction(r, c, dr, dc):
                    count += 1

    return count


def read_input_as_matrix(file_path: str) -> ndarray[Any, dtype[Any]]:
    with open(file_path, "r") as file:
        return np.array([list(row) for row in file.read().strip().split("\n")])

def part_one() -> int:
    word = "XMAS"
    matrix = read_input_as_matrix(file_name)
    return count_word_in_matrix(matrix, word)


def check_x(matrix, i, j, valid_patterns):
    # Build the string representing the X
    x_string = (
            matrix[i - 1, j - 1] + matrix[i, j] + matrix[i + 1, j + 1] +
            matrix[i - 1, j + 1] + matrix[i, j] + matrix[i + 1, j - 1]
    )
    # Return whether the X string is in the valid patterns
    return x_string in valid_patterns


def count_xmas(matrix):
    valid_patterns = {"MASMAS", "SAMSAM", "SAMMAS", "MASSAM"}  # Valid X-MAS patterns
    rows, cols = matrix.shape
    count = 0

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if matrix[i, j] == "A":
                count += int(check_x(matrix, i, j, valid_patterns))

    return count


def part_two() -> int:
    matrix = read_input_as_matrix(file_name)
    result = count_xmas(matrix)
    return result

def day_four():
    part_one_solution = part_one()
    part_two_solution = part_two()

    assert part_one_solution == 2414
    # assert part_two_solution == 3494

    print(part_one_solution)
    print(part_two_solution)

if __name__ == "__main__":
    day_four()
