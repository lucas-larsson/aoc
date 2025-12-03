def find_max_joltage(bank: str) -> int:
    """
    Find the maximum joltage possible from a bank of batteries.
    We need to select exactly 2 batteries and the joltage is the 2-digit number formed.
    """
    max_joltage = 0

    # Try all pairs of positions (i, j) where i < j
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form the 2-digit number
            joltage = int(bank[i] + bank[j])
            max_joltage = max(max_joltage, joltage)

    return max_joltage

def part_one(banks: list) -> int:
    """Calculate the total output joltage from all banks."""
    total = 0

    for bank in banks:
        max_joltage = find_max_joltage(bank)
        total += max_joltage

    return total

def find_max_joltage_12(bank: str) -> int:
    """
    Find the maximum joltage by selecting exactly 12 batteries.
    Uses a greedy approach: at each position, pick the largest digit
    that still leaves enough digits to complete the selection.
    """
    n = len(bank)
    if n < 12:
        return 0  # Can't select 12 digits

    result = []
    start = 0

    for i in range(12):
        # For the i-th position in our result, we need (12 - i) digits total
        # After selecting this digit, we need (12 - i - 1) more
        # So we can look ahead at most to position: n - (12 - i)
        max_end = n - (12 - i) + 1

        # Find the maximum digit in the valid range
        max_digit = max(bank[start:max_end])

        # Find the first occurrence of this max digit in range
        max_pos = bank.index(max_digit, start, max_end)

        result.append(max_digit)
        start = max_pos + 1

    return int(''.join(result))

def part_two(banks: list) -> int:
    """Calculate the total output joltage with 12-battery selection."""
    total = 0

    for bank in banks:
        max_joltage = find_max_joltage_12(bank)
        total += max_joltage

    return total

def day_three():
    file_name = "../input/day_03.txt"

    with open(file_name, 'r') as f:
        banks = [line.strip() for line in f if line.strip()]

    part_one_solution = part_one(banks)
    part_two_solution = part_two(banks)

    print(f"Part 1: {part_one_solution}")
    print(f"Part 2: {part_two_solution}")

if __name__ == "__main__":
    day_three()