def is_invalid_id(num: int) -> bool:
    """
    Check if a number is invalid (made of some sequence repeated twice).
    For example: 55, 6464, 123123 are invalid.
    """
    s = str(num)
    length = len(s)

    # Must have even length to be split into two equal parts
    if length % 2 != 0:
        return False

    # Check if first half equals second half
    mid = length // 2
    return s[:mid] == s[mid:]

def is_invalid_id_v2(num: int) -> bool:
    """
    Check if a number is invalid (made of some sequence repeated at least twice).
    For example: 123123 (2 times), 123123123 (3 times), 1111111 (7 times) are all invalid.
    """
    s = str(num)
    length = len(s)

    # Try all possible pattern lengths
    # Pattern must repeat at least twice, so max pattern length is length // 2
    for pattern_length in range(1, length // 2 + 1):
        # Check if this pattern length divides evenly into the total length
        if length % pattern_length == 0:
            repetitions = length // pattern_length
            # Must repeat at least twice
            if repetitions >= 2:
                pattern = s[:pattern_length]
                # Check if repeating this pattern gives us the full string
                if pattern * repetitions == s:
                    return True

    return False

def parse_ranges(input_str: str) -> list:
    """Parse the input string into list of (start, end) tuples."""
    ranges = []
    parts = input_str.strip().split(',')
    for part in parts:
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
    return ranges

def part_one(ranges: list) -> int:
    """Find and sum all invalid product IDs in the given ranges."""
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total += num

    return total

def part_two(ranges: list) -> int:
    """Find and sum all invalid product IDs using the new rules (at least 2 repetitions)."""
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id_v2(num):
                total += num

    return total

def day_two():
    file_name = "../input/day_02.txt"

    with open(file_name, 'r') as f:
        input_data = f.read()

    ranges = parse_ranges(input_data)

    part_one_solution = part_one(ranges)
    part_two_solution = part_two(ranges)

    print(f"Part 1: {part_one_solution}")
    print(f"Part 2: {part_two_solution}")

if __name__ == "__main__":
    day_two()