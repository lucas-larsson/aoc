def part_one(lines: list) -> int:
    blank_index = lines.index('')

    # Parse fresh ingredient ranges
    fresh_ranges = []
    for line in lines[:blank_index]:
        start, end = map(int, line.split('-'))
        fresh_ranges.append((start, end))

    # Parse available ingredient IDs
    available_ids = []
    for line in lines[blank_index + 1:]:
        available_ids.append(int(line))

    # Count how many available IDs are fresh
    fresh_count = 0
    for ingredient_id in available_ids:
        # Check if this ID falls within any fresh range
        for start, end in fresh_ranges:
            if start <= ingredient_id <= end:
                fresh_count += 1
                break  # No need to check other ranges once we find a match

    return fresh_count


def part_one_optimized(lines: list) -> int:
    """Pythonic/competitive programming style solution using comprehensions and any()"""
    blank_index = lines.index('')

    # Parse using list comprehensions
    fresh_ranges = [tuple(map(int, line.split('-'))) for line in lines[:blank_index]]
    available_ids = [int(line) for line in lines[blank_index + 1:]]

    # Using sum() with any() - counts True values (True = 1, False = 0)
    return sum(any(start <= id <= end for start, end in fresh_ranges) for id in available_ids)


def part_one_numpy(lines: list) -> int:
    """Using NumPy for vectorized C-level operations"""
    import numpy as np

    blank_index = lines.index('')

    # Parse ranges into NumPy arrays
    ranges = np.array([list(map(int, line.split('-'))) for line in lines[:blank_index]])
    ids = np.array([int(line) for line in lines[blank_index + 1:]])

    # Vectorized comparison: check each ID against all ranges at once
    # ids[:, None] creates a column vector, ranges creates a 2D array
    # This broadcasts the comparison across all combinations
    count = 0
    for id_val in ids:
        if np.any((id_val >= ranges[:, 0]) & (id_val <= ranges[:, 1])):
            count += 1

    return count


def part_one_bisect(lines: list) -> int:
    """Using bisect (C-backed binary search) with merged intervals"""
    import bisect

    blank_index = lines.index('')

    # Parse and sort ranges
    fresh_ranges = [tuple(map(int, line.split('-'))) for line in lines[:blank_index]]
    fresh_ranges.sort()

    # Merge overlapping ranges
    merged = [fresh_ranges[0]]
    for start, end in fresh_ranges[1:]:
        if start <= merged[-1][1] + 1:  # Overlapping or adjacent
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    available_ids = [int(line) for line in lines[blank_index + 1:]]

    # Use binary search to find where each ID would fit
    count = 0
    for id_val in available_ids:
        # Find the rightmost range that starts <= id_val
        idx = bisect.bisect_right([r[0] for r in merged], id_val) - 1
        if idx >= 0 and merged[idx][0] <= id_val <= merged[idx][1]:
            count += 1

    return count

def part_two(lines: list) -> int:
    """Count total unique ingredient IDs covered by all ranges - Original approach"""
    blank_index = lines.index('')

    # Parse and sort ranges
    fresh_ranges = [tuple(map(int, line.split('-'))) for line in lines[:blank_index]]
    fresh_ranges.sort()

    # Merge overlapping ranges
    merged = [fresh_ranges[0]]
    for start, end in fresh_ranges[1:]:
        if start <= merged[-1][1] + 1:  # Overlapping or adjacent
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    # Count total IDs in all merged ranges
    # For a range (start, end), there are (end - start + 1) IDs
    total = sum(end - start + 1 for start, end in merged)

    return total


def part_two_reduce(lines: list) -> int:
    """Using functools.reduce - functional programming style"""
    from functools import reduce

    blank_index = lines.index('')
    fresh_ranges = sorted(tuple(map(int, line.split('-'))) for line in lines[:blank_index])

    # Merge using reduce - accumulator is the list of merged ranges
    def merge_ranges(merged, current):
        start, end = current
        if merged and start <= merged[-1][1] + 1:
            # Extend last range
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # Add new range
            merged.append((start, end))
        return merged

    merged = reduce(merge_ranges, fresh_ranges, [])
    return sum(end - start + 1 for start, end in merged)


def part_two_itertools(lines: list) -> int:
    """Using itertools for pairwise comparisons"""
    from itertools import pairwise

    blank_index = lines.index('')
    fresh_ranges = sorted(tuple(map(int, line.split('-'))) for line in lines[:blank_index])

    merged = [fresh_ranges[0]]
    for _, (curr_start, curr_end) in pairwise(fresh_ranges):
        # Compare with the last merged range, not the previous input range
        if curr_start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], curr_end))
        else:
            merged.append((curr_start, curr_end))

    return sum(end - start + 1 for start, end in merged)


def part_two_walrus(lines: list) -> int:
    """Using walrus operator for inline assignments"""
    blank_index = lines.index('')
    fresh_ranges = sorted(tuple(map(int, line.split('-'))) for line in lines[:blank_index])

    merged = [fresh_ranges[0]]
    for start, end in fresh_ranges[1:]:
        # Use walrus to capture last range while checking condition
        if start <= (last := merged[-1])[1] + 1:
            merged[-1] = (last[0], max(last[1], end))
        else:
            merged.append((start, end))

    return sum(end - start + 1 for start, end in merged)


def part_two_oneliner(lines: list) -> int:
    """Compact competitive programming style - prioritizes brevity"""
    from functools import reduce
    blank_index = lines.index('')
    ranges = sorted(tuple(map(int, line.split('-'))) for line in lines[:blank_index])
    merged = reduce(lambda m, r: m[:-1] + [(m[-1][0], max(m[-1][1], r[1]))] if r[0] <= m[-1][1] + 1 else m + [r], ranges[1:], [ranges[0]])
    return sum(e - s + 1 for s, e in merged)

def day_five():
    import time

    file_name = "../input/day_05.txt"
    with open(file_name, 'r') as f:
        lines = f.read().strip().split('\n')

    # Run and time Part 1 versions
    print("=" * 60)
    print("PART 1 - Finding fresh ingredients from available list")
    print("=" * 60)
    part1_versions = [
        ("Original (for loops)", part_one),
        ("Pythonic (any/sum)", part_one_optimized),
        ("NumPy (vectorized C)", part_one_numpy),
        ("Bisect (binary search)", part_one_bisect),
    ]

    results = []
    for name, func in part1_versions:
        start = time.perf_counter()
        result = func(lines)
        elapsed = time.perf_counter() - start
        results.append((name, result, elapsed))

    baseline = results[0][2]
    for name, result, elapsed in results:
        speedup = baseline / elapsed
        print(f"  {name:25s}: {result} ({elapsed*1000:6.3f} ms, {speedup:5.2f}x)")

    # Run and time Part 2 versions
    print("\n" + "=" * 60)
    print("PART 2 - Counting total IDs in merged ranges")
    print("=" * 60)
    part2_versions = [
        ("Original (for loop)", part_two),
        ("Reduce (functional)", part_two_reduce),
        ("Itertools (pairwise)", part_two_itertools),
        ("Walrus operator", part_two_walrus),
        ("One-liner (compact)", part_two_oneliner),
    ]

    results2 = []
    for name, func in part2_versions:
        start = time.perf_counter()
        result = func(lines)
        elapsed = time.perf_counter() - start
        results2.append((name, result, elapsed))

    baseline2 = results2[0][2]
    for name, result, elapsed in results2:
        speedup = baseline2 / elapsed
        print(f"  {name:25s}: {result} ({elapsed*1000:6.3f} ms, {speedup:5.2f}x)")


if __name__ == "__main__":
    day_five()
