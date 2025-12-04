import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button, Slider
import sys

class InteractivePaperAnimator:
    """Interactive animated visualization with speed controls"""

    def __init__(self, grid: list):
        self.original_grid = [list(row) for row in grid]
        self.grid = np.array([list(row) for row in grid])
        self.rows, self.cols = self.grid.shape
        self.directions = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),           (0, 1),
                          (1, -1),  (1, 0),  (1, 1)]

        self.frames = []
        self.round_info = []
        self.compute_all_frames()

        # Animation state
        self.current_frame = 0
        self.playing = True
        self.anim = None

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
        numeric = np.zeros((self.rows, self.cols))
        for row in range(self.rows):
            for col in range(self.cols):
                if highlight_positions and (row, col) in highlight_positions:
                    numeric[row, col] = 2
                elif self.grid[row, col] == '@':
                    numeric[row, col] = 1
                else:
                    numeric[row, col] = 0
        return numeric

    def compute_all_frames(self):
        round_num = 0
        total_removed = 0

        # Initial state
        self.frames.append(self.grid_to_numeric())
        self.round_info.append(f"Initial: {np.sum(self.grid == '@')} paper rolls")

        while True:
            accessible = self.get_accessible_positions()
            if not accessible:
                remaining = np.sum(self.grid == '@')
                self.round_info.append(f"DONE! Removed: {total_removed} | Remaining: {remaining}")
                break

            round_num += 1

            # Show accessible
            self.frames.append(self.grid_to_numeric(accessible))
            self.round_info.append(f"Round {round_num}: {len(accessible)} accessible")

            # Remove
            for row, col in accessible:
                self.remove_roll(row, col)
            total_removed += len(accessible)

            # After removal
            self.frames.append(self.grid_to_numeric())
            remaining = np.sum(self.grid == '@')
            self.round_info.append(f"Removed {len(accessible)} | Total: {total_removed} | Remaining: {remaining}")

    def create_animation(self, interval=500):
        colors = ['#0f0f23', '#00cc66', '#ff3366']
        cmap = ListedColormap(colors)

        # Create figure with better spacing
        fig = plt.figure(figsize=(14, 13))

        # Main grid display
        ax = plt.axes([0.1, 0.25, 0.8, 0.65])

        # Plot
        im = ax.imshow(self.frames[0], cmap=cmap, interpolation='nearest', vmin=0, vmax=2)
        ax.set_xticks([])
        ax.set_yticks([])

        # Title - positioned above the grid with more space
        title = fig.text(0.5, 0.92, self.round_info[0],
                        ha='center', va='top',
                        fontsize=13, fontweight='bold', family='monospace',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        # Frame counter - top right
        frame_counter = fig.text(0.9, 0.95, f"Frame: 1/{len(self.frames)}",
                                ha='right', va='top',
                                fontsize=11, family='monospace',
                                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#0f0f23', label='Empty'),
            Patch(facecolor='#00cc66', label='Paper Roll'),
            Patch(facecolor='#ff3366', label='Accessible')
        ]
        ax.legend(handles=legend_elements, loc='upper center',
                 bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False, fontsize=10)

        # Grid lines
        if self.rows <= 50:  # Only show grid for smaller grids
            ax.set_xticks(np.arange(-0.5, self.cols, 1), minor=True)
            ax.set_yticks(np.arange(-0.5, self.rows, 1), minor=True)
            ax.grid(which='minor', color='#333333', linewidth=0.3, alpha=0.5)

        # Progress bar
        ax_progress = plt.axes([0.1, 0.17, 0.8, 0.02])
        ax_progress.set_xlim(0, len(self.frames))
        ax_progress.set_ylim(0, 1)
        ax_progress.set_xticks([])
        ax_progress.set_yticks([])
        progress_bar = ax_progress.barh(0.5, 1, height=0.8, color='#00cc66', alpha=0.7)
        progress_text = ax_progress.text(0.5, 0.5, '0%', ha='center', va='center',
                                        fontsize=10, fontweight='bold', color='white')

        # Control buttons - positioned at the bottom
        ax_play = plt.axes([0.25, 0.08, 0.1, 0.04])
        ax_reset = plt.axes([0.37, 0.08, 0.1, 0.04])
        ax_next = plt.axes([0.49, 0.08, 0.1, 0.04])
        ax_prev = plt.axes([0.61, 0.08, 0.1, 0.04])
        ax_speed = plt.axes([0.25, 0.03, 0.5, 0.03])

        btn_play = Button(ax_play, 'Pause')
        btn_reset = Button(ax_reset, 'Reset')
        btn_next = Button(ax_next, 'Next →')
        btn_prev = Button(ax_prev, '← Prev')
        slider_speed = Slider(ax_speed, 'Speed', 0.1, 2.0, valinit=1.0, valstep=0.1)

        def update(frame):
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

            # Update image
            im.set_array(self.frames[self.current_frame])

            # Update title
            title.set_text(self.round_info[self.current_frame])

            # Update frame counter
            frame_counter.set_text(f"Frame: {self.current_frame + 1}/{len(self.frames)}")

            # Update progress bar
            progress_pct = (self.current_frame + 1) / len(self.frames)
            progress_bar[0].set_width(self.current_frame + 1)
            progress_text.set_text(f"{int(progress_pct * 100)}%")
            progress_text.set_x((self.current_frame + 1) / 2)

            if self.playing:
                self.current_frame += 1

            return [im, title, frame_counter, progress_bar[0], progress_text]

        def toggle_play(event):
            self.playing = not self.playing
            btn_play.label.set_text('Play' if not self.playing else 'Pause')

        def reset(event):
            self.current_frame = 0
            self.playing = False
            btn_play.label.set_text('Play')

        def next_frame(event):
            self.playing = False
            btn_play.label.set_text('Play')
            self.current_frame = min(self.current_frame + 1, len(self.frames) - 1)

        def prev_frame(event):
            self.playing = False
            btn_play.label.set_text('Play')
            self.current_frame = max(self.current_frame - 1, 0)

        def update_speed(val):
            if self.anim:
                self.anim.event_source.interval = interval / val

        btn_play.on_clicked(toggle_play)
        btn_reset.on_clicked(reset)
        btn_next.on_clicked(next_frame)
        btn_prev.on_clicked(prev_frame)
        slider_speed.on_changed(update_speed)

        self.anim = animation.FuncAnimation(
            fig, update,
            frames=len(self.frames) * 2,
            interval=interval,
            blit=False,  # Disable blit to avoid issues with custom UI
            repeat=True
        )

        plt.show()


def main():
    print("\n" + "="*70)
    print("INTERACTIVE PAPER ROLL REMOVAL VISUALIZATION")
    print("="*70)

    # Ask which grid to visualize
    print("\nSelect grid to visualize:")
    print("  1. Example grid (10x10)")
    print("  2. Your actual puzzle input")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == '1':
        grid = [
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
        print("\nLoading example grid...")
    else:
        with open("../input/day_04.txt", 'r') as f:
            grid = [line.strip() for line in f.readlines()]
        print(f"\nLoading actual puzzle ({len(grid)}x{len(grid[0])})...")

    print("Computing animation frames...")
    animator = InteractivePaperAnimator(grid)

    print(f"\nAnimation ready!")
    print(f"  Total frames: {len(animator.frames)}")
    print(f"  Total rounds: {len(animator.frames) // 2}")
    print("\nControls:")
    print("  • Play/Pause button: Toggle animation")
    print("  • Reset button: Go back to start")
    print("  • Next → button: Advance one frame forward")
    print("  • ← Prev button: Go back one frame")
    print("  • Speed slider: Adjust playback speed (0.1x - 2.0x)")
    print("  • Progress bar: Shows current position in animation")
    print("  • Frame counter: Top-right shows current frame number")
    print("  • Close window to exit")
    print("="*70 + "\n")

    animator.create_animation(interval=500)


if __name__ == "__main__":
    main()