
def count_increasing_violations(row):
    """Counts the number of violations in the increasing rule."""
    return sum(1 for i in range(len(row) - 1) if not (row[i] < row[i+1])) <= 1

def count_decreasing_violations(row):
    """Counts the number of violations in the decreasing rule."""
    return sum(1 for i in range(len(row) - 1) if not (row[i] > row[i+1])) <= 1

def count_difference_violations(row):
    """Counts the number of violations in the adjacent difference rule."""
    return sum(1 for i in range(len(row) - 1) if not (1 <= abs(row[i] - row[i+1]) <= 3)) <= 1

def is_safe(row):
    increasing = all(row[i] < row[i + 1] for i in range(len(row) - 1))
    decreasing = all(row[i] > row[i + 1] for i in range(len(row) - 1))
    valid_differences = all(1 <= abs(row[i] - row[i + 1]) <= 3 for i in range(len(row) - 1))
    return (increasing or decreasing) and valid_differences


def is_safe_with_one_violation(row):
    increasing = count_increasing_violations(row)
    decreasing = count_decreasing_violations(row)
    valid_differences = count_difference_violations(row)
    return (increasing or decreasing) and valid_differences

def count_safe_rows(file_path, part):
    safe_count = 0

    with open(file_path, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            # if part == 1:
            #     if is_safe(row):
            #         safe_count += 1
            if part == 2:
                if is_safe_with_one_violation(row):
                    safe_count += 1
    return safe_count



def part_one(file_path) -> int:
    return count_safe_rows(file_path, 1)

def part_two(file_path) -> int:
    return count_safe_rows(file_path, 2)

# --------------
def is_safe(row):
    """Check if a row is safe according to the monotonicity and adjacent difference rules."""
    increasing = all(row[i] < row[i + 1] for i in range(len(row) - 1))
    decreasing = all(row[i] > row[i + 1] for i in range(len(row) - 1))
    valid_differences = all(1 <= abs(row[i] - row[i + 1]) <= 3 for i in range(len(row) - 1))
    return (increasing or decreasing) and valid_differences


def is_safe_with_dampener(row):
    if is_safe(row):
        return True

    for i in range(len(row)):
        new_row = row[:i] + row[i + 1:]
        if is_safe(new_row):
            return True
    return False


def count_safe_reports_with_dampener(file_path):
    """Count the number of safe reports, considering the Problem Dampener."""
    safe_count = 0

    with open(file_path, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            if is_safe_with_dampener(row):
                safe_count += 1

    return safe_count


file_path = "../input/day_02.txt"
safe_reports = count_safe_reports_with_dampener(file_path)
print(f"Number of safe reports (with Problem Dampener): {safe_reports}")

# --------------
if __name__ == "__main__":
    file_path = "../input/day_02.txt"

    # solution_part_one = part_one(file_path)
    # solution_part_two = part_two(file_path)
    # assert solution_part_one == 680
    # assert solution_part_two == 210
    safe_reports = count_safe_reports_with_dampener(file_path)
    print(f"Number of safe reports (with Problem Dampener): {safe_reports}")

    # print(f"Number of safe rows for part one: {solution_part_one}")
    # print(f"Number of safe rows for part two: {solution_part_two}")
