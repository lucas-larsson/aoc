def read_rotations(file_path: str) -> list:
    """Read rotation instructions from the input file."""
    rotations = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            direction = line[0]  # 'L' or 'R'
            distance = int(line[1:])  # The number after the direction
            rotations.append((direction, distance))
    return rotations

def part_one(rotations: list) -> int:
    """
    Simulate the dial rotations and count how many times
    the dial lands on 0 after any rotation.
    """
    position = 50  # Starting position
    count = 0

    for direction, distance in rotations:
        if direction == 'L':
            # Rotate left (toward lower numbers)
            position = (position - distance) % 100
        else:  # direction == 'R'
            # Rotate right (toward higher numbers)
            position = (position + distance) % 100

        # Check if we landed on 0
        if position == 0:
            count += 1

    return count

def part_two(rotations: list) -> int:
    """
    Count the number of times the dial points at 0 during any click,
    including both during rotations and at the end of rotations.
    """
    position = 50  # Starting position
    count = 0

    for direction, distance in rotations:
        if direction == 'R':
            # Right rotation: we hit 0 when (position + k) % 100 == 0
            # This happens at k = 100-position, 200-position, etc.
            # Number of times = (position + distance) // 100
            count += (position + distance) // 100
            position = (position + distance) % 100
        else:  # direction == 'L'
            # Left rotation: we hit 0 when (position - k) % 100 == 0
            # This happens at k = position, position+100, position+200, etc.
            # Special case: if starting at 0, we hit 0 at: 100, 200, 300, ...
            if position == 0:
                count += distance // 100
            else:
                if distance >= position:
                    count += 1 + (distance - position) // 100
            position = (position - distance) % 100

    return count

def day_one():
    file_name = "../input/day_01.txt"
    rotations = read_rotations(file_name)

    part_one_solution = part_one(rotations)
    part_two_solution = part_two(rotations)

    print(f"Part 1: {part_one_solution}")
    print(f"Part 2: {part_two_solution}")


if __name__ == "__main__":
    day_one()
