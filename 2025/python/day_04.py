import numpy as np

class PaperGrid:
    """Custom data structure for managing the paper roll grid"""

    def __init__(self, grid: list):
        # Convert list of strings to a proper 2D NumPy array
        self.grid = np.array([list(row) for row in grid])
        self.rows, self.cols = self.grid.shape
        # Define 8 directions: up-left, up, up-right, left, right, down-left, down, down-right
        self.directions = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),           (0, 1),
                          (1, -1),  (1, 0),  (1, 1)]

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is within grid boundaries"""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_paper_roll(self, row: int, col: int) -> bool:
        """Check if there's a paper roll at the given position"""
        return self.is_valid_position(row, col) and self.grid[row, col] == '@'

    def count_adjacent_rolls(self, row: int, col: int) -> int:
        """Count paper rolls in the 8 adjacent positions"""
        count = 0
        for dr, dc in self.directions:
            neighbor_row = row + dr
            neighbor_col = col + dc
            if self.is_paper_roll(neighbor_row, neighbor_col):
                count += 1
        return count

    def is_accessible(self, row: int, col: int) -> bool:
        """A roll is accessible if it has fewer than 4 adjacent rolls"""
        if not self.is_paper_roll(row, col):
            return False
        return self.count_adjacent_rolls(row, col) < 4

    def count_accessible_rolls(self) -> int:
        """Count all paper rolls that can be accessed by forklifts"""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_accessible(row, col):
                    count += 1
        return count

    def get_accessible_positions(self) -> list:
        """Get list of all accessible roll positions"""
        positions = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_accessible(row, col):
                    positions.append((row, col))
        return positions

    def remove_roll(self, row: int, col: int):
        """Remove a paper roll from the grid"""
        if self.is_valid_position(row, col):
            self.grid[row, col] = '.'

    def print_grid(self, accessible_positions=None):
        """Print the grid with optional highlighting of accessible positions"""
        for row in range(self.rows):
            line = ""
            for col in range(self.cols):
                if accessible_positions and (row, col) in accessible_positions:
                    # Highlight accessible positions that are about to be removed
                    line += '\033[91m@\033[0m'  # Red @ for accessible
                elif self.grid[row, col] == '@':
                    line += '@'
                elif self.grid[row, col] == '.':
                    line += '.'
                else:
                    line += self.grid[row, col]
            print(line)
        print()

    def simulate_removal(self, visualize=False) -> int:
        """Simulate iterative removal of accessible rolls until none remain"""
        total_removed = 0
        round_num = 0

        if visualize:
            print("Initial state:")
            self.print_grid()

        while True:
            # Find all currently accessible rolls
            accessible = self.get_accessible_positions()

            # If no more accessible rolls, we're done
            if not accessible:
                break

            round_num += 1

            if visualize:
                print(f"Round {round_num}: Removing {len(accessible)} rolls (shown in red):")
                self.print_grid(accessible)
                input("Press Enter to continue...")

            # Remove all accessible rolls
            for row, col in accessible:
                self.remove_roll(row, col)

            # Count how many we removed this round
            total_removed += len(accessible)

            if visualize:
                print(f"After removal:")
                self.print_grid()

        if visualize:
            print(f"Total removed: {total_removed}")

        return total_removed


def part_one(grid: list) -> int:
    paper_grid = PaperGrid(grid)
    return paper_grid.count_accessible_rolls()

def part_two(grid: list) -> int:
    paper_grid = PaperGrid(grid)
    return paper_grid.simulate_removal()

def day_four():
    file_name = "../input/day_04.txt"

    # Read the grid
    with open(file_name, 'r') as file:
        grid = [line.strip() for line in file.readlines()]

    part_one_solution = part_one(grid)
    part_two_solution = part_two(grid)

    print(f"Part 1: {part_one_solution}")
    print(f"Part 2: {part_two_solution}")

if __name__ == "__main__":
    day_four()