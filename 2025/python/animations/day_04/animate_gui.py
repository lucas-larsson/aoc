import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import copy

class PaperGridAnimator:
    """Animated visualization of paper roll removal"""

    def __init__(self, grid: list):
        self.original_grid = [list(row) for row in grid]
        self.grid = np.array([list(row) for row in grid])
        self.rows, self.cols = self.grid.shape
        self.directions = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),           (0, 1),
                          (1, -1),  (1, 0),  (1, 1)]

        # Storage for animation frames
        self.frames = []
        self.round_info = []
        self.compute_all_frames()

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_paper_roll(self, row: int, col: int) -> bool:
        return self.is_valid_position(row, col) and self.grid[row, col] == '@'

    def count_adjacent_rolls(self, row: int, col: int) -> int:
        count = 0
        for dr, dc in self.directions:
            if self.is_paper_roll(row + dr, col + dc):
                count += 1
        return count

    def is_accessible(self, row: int, col: int) -> bool:
        if not self.is_paper_roll(row, col):
            return False
        return self.count_adjacent_rolls(row, col) < 4

    def get_accessible_positions(self) -> list:
        positions = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_accessible(row, col):
                    positions.append((row, col))
        return positions

    def remove_roll(self, row: int, col: int):
        if self.is_valid_position(row, col):
            self.grid[row, col] = '.'

    def grid_to_numeric(self, highlight_positions=None):
        """Convert grid to numeric array for visualization
        0 = empty, 1 = paper roll, 2 = accessible (to be removed)
        """
        numeric = np.zeros((self.rows, self.cols))
        for row in range(self.rows):
            for col in range(self.cols):
                if highlight_positions and (row, col) in highlight_positions:
                    numeric[row, col] = 2  # Accessible (red)
                elif self.grid[row, col] == '@':
                    numeric[row, col] = 1  # Paper roll (green)
                else:
                    numeric[row, col] = 0  # Empty (dark)
        return numeric

    def compute_all_frames(self):
        """Pre-compute all animation frames"""
        round_num = 0
        total_removed = 0

        # Initial state
        self.frames.append(self.grid_to_numeric())
        self.round_info.append(f"Initial State - {np.sum(self.grid == '@')} paper rolls")

        while True:
            accessible = self.get_accessible_positions()

            if not accessible:
                # Final state
                remaining = np.sum(self.grid == '@')
                self.round_info.append(f"COMPLETE! Removed: {total_removed}, Remaining: {remaining}")
                break

            round_num += 1

            # Frame showing accessible positions
            self.frames.append(self.grid_to_numeric(accessible))
            self.round_info.append(f"Round {round_num}: Found {len(accessible)} accessible rolls")

            # Remove rolls
            for row, col in accessible:
                self.remove_roll(row, col)

            total_removed += len(accessible)

            # Frame after removal
            self.frames.append(self.grid_to_numeric())
            remaining = np.sum(self.grid == '@')
            self.round_info.append(f"After Round {round_num}: Removed {len(accessible)}, Total: {total_removed}, Remaining: {remaining}")

    def animate(self, interval=800, save_as=None):
        """Create and display animation"""
        # Create custom colormap
        colors = ['#1a1a2e', '#16a085', '#e74c3c']  # Dark blue, green, red
        cmap = ListedColormap(colors)

        fig, ax = plt.subplots(figsize=(12, 12))

        # Initial plot
        im = ax.imshow(self.frames[0], cmap=cmap, interpolation='nearest', vmin=0, vmax=2)
        ax.set_xticks([])
        ax.set_yticks([])

        # Title
        title = ax.text(0.5, 1.05, self.round_info[0],
                       ha='center', va='bottom', transform=ax.transAxes,
                       fontsize=14, fontweight='bold', family='monospace')

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#1a1a2e', label='Empty'),
            Patch(facecolor='#16a085', label='Paper Roll (Protected)'),
            Patch(facecolor='#e74c3c', label='Accessible (Will Remove)')
        ]
        ax.legend(handles=legend_elements, loc='upper left',
                 bbox_to_anchor=(0, -0.05), ncol=3, frameon=False)

        # Add grid
        ax.set_xticks(np.arange(-0.5, self.cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.rows, 1), minor=True)
        ax.grid(which='minor', color='#2c3e50', linewidth=0.5, alpha=0.3)

        frame_index = [0]  # Use list to modify in nested function

        def update(frame):
            if frame_index[0] < len(self.frames):
                im.set_array(self.frames[frame_index[0]])
                title.set_text(self.round_info[frame_index[0]])
                frame_index[0] += 1
                return [im, title]
            return [im, title]

        # Create animation
        anim = animation.FuncAnimation(
            fig, update,
            frames=len(self.frames),
            interval=interval,
            blit=True,
            repeat=True
        )

        if save_as:
            print(f"Saving animation to {save_as}...")
            anim.save(save_as, writer='pillow', fps=1)
            print("Done!")

        plt.tight_layout()
        plt.show()


# Example grid
example_grid = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@."
]

print("\n" + "="*60)
print("PAPER ROLL REMOVAL - ANIMATED VISUALIZATION")
print("="*60)
print("\nControls:")
print("  • Close the window to stop")
print("  • Animation will loop automatically")
print("  • Each frame pauses for 0.8 seconds")
print("\nLegend:")
print("  • Dark blue = Empty space")
print("  • Green = Paper rolls (protected)")
print("  • Red = Accessible rolls (about to be removed)")
print("="*60 + "\n")

print("Creating animation...")
animator = PaperGridAnimator(example_grid)

print(f"Total frames: {len(animator.frames)}")
print(f"Total rounds: {len(animator.frames) // 2}")
print("\nStarting visualization window...")
print("(Close the window when done)\n")

# Animate with 800ms between frames (adjustable)
animator.animate(interval=800)

# To save as GIF, uncomment:
# animator.animate(interval=800, save_as='paper_removal.gif')