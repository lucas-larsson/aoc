def solve_with_lists(grid, debug=False):
    """
    Simple approach using lists to track beams.
    Each beam starts at a position and moves downward until hitting a splitter or boundary.
    """
    # Find starting position 'S'
    start_row, start_col = None, None
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break

    split_splitters = set()  # Track which splitters have been split
    visited = set()  # Track which starting positions we've already processed
    beams = [(start_row, start_col)]  # List of (row, col) positions to process

    while beams:
        new_beams = []

        for row, col in beams:
            # Skip if we've already processed a beam from this position
            if (row, col) in visited:
                continue
            visited.add((row, col))

            # Move beam downward until hitting splitter or boundary
            current_row = row + 1
            while current_row < len(grid):
                if col < len(grid[current_row]) and grid[current_row][col] == '^':
                    # Hit a splitter!
                    splitter_pos = (current_row, col)
                    if splitter_pos not in split_splitters:
                        split_splitters.add(splitter_pos)
                        if debug:
                            print(f"Split #{len(split_splitters)}: Beam from ({row},{col}) hit splitter at {splitter_pos}")
                    else:
                        if debug:
                            print(f"Beam from ({row},{col}) hit already-split splitter at {splitter_pos}")
                    # Create two new beams at positions left and right of splitter
                    if col - 1 >= 0:
                        new_beams.append((current_row, col - 1))
                    if col + 1 < len(grid[current_row]):
                        new_beams.append((current_row, col + 1))
                    break
                current_row += 1

        beams = new_beams

    return len(split_splitters)


def solve_with_queue(grid):
    """
    Queue-based approach using collections.deque for BFS-style processing.
    More efficient for larger inputs.
    """
    from collections import deque

    # Find starting position 'S'
    start_row, start_col = None, None
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break

    split_splitters = set()  # Track which splitters have been split
    visited = set()
    queue = deque([(start_row, start_col)])

    while queue:
        row, col = queue.popleft()

        # Skip if we've already processed a beam from this position
        if (row, col) in visited:
            continue
        visited.add((row, col))

        # Move beam downward until hitting splitter or boundary
        current_row = row + 1
        while current_row < len(grid):
            if col < len(grid[current_row]) and grid[current_row][col] == '^':
                # Hit a splitter!
                splitter_pos = (current_row, col)
                split_splitters.add(splitter_pos)
                # Create two new beams at positions left and right of splitter
                if col - 1 >= 0:
                    queue.append((current_row, col - 1))
                if col + 1 < len(grid[current_row]):
                    queue.append((current_row, col + 1))
                break
            current_row += 1

    return len(split_splitters)


def part_one(grid):
    return solve_with_queue(grid)


def part_two(grid):
    """
    Count the number of timelines using recursive DFS with memoization.
    Each splitter splits the timeline in two (left and right).
    """
    # Find starting position 'S'
    start_row, start_col = None, None
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break

    memo = {}

    def dfs(row, col):
        """
        Returns the number of timelines starting from position (row, col).
        """
        # Check if we've already computed this position
        if (row, col) in memo:
            return memo[(row, col)]

        # Check if position is out of bounds
        if col < 0 or col >= len(grid[0]):
            return 0

        # Move downward until hitting splitter or exiting grid
        current_row = row + 1
        while current_row < len(grid):
            if col < len(grid[current_row]) and grid[current_row][col] == '^':
                # Hit a splitter - timeline splits into left and right
                left_timelines = dfs(current_row, col - 1)
                right_timelines = dfs(current_row, col + 1)
                result = left_timelines + right_timelines
                memo[(row, col)] = result
                return result
            current_row += 1

        # Exited the grid - this is one complete timeline
        memo[(row, col)] = 1
        return 1

    return dfs(start_row, start_col)


def day_seven():
    # Test with the test file first
    test_file = "../input/day_07_test.txt"
    with open(test_file, "r") as file:
        test_grid = [line.strip() for line in file.readlines()]

    print("Testing with day_07_test.txt:")
    print("Part 1 Tests:")
    test_result_lists = solve_with_lists(test_grid, debug=False)
    print(f"  List approach: {test_result_lists} splits")

    test_result_queue = solve_with_queue(test_grid)
    print(f"  Queue approach: {test_result_queue} splits")
    print(f"  Expected: 21 splits")

    print("\nPart 2 Test:")
    test_part_two = part_two(test_grid)
    print(f"  Timelines: {test_part_two}")
    print(f"  Expected: 40 timelines")
    print()

    # Now solve the actual puzzle
    file_name = "../input/day_07.txt"
    with open(file_name, "r") as file:
        grid = [line.strip() for line in file.readlines()]

    part_one_solution = part_one(grid)
    part_two_solution = part_two(grid)

    print(f"Part 1: {part_one_solution}")
    print(f"Part 2: {part_two_solution}")


if __name__ == "__main__":
    day_seven()
