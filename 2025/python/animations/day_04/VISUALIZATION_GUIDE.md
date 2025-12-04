# Paper Roll Removal Visualization Guide

**Day 4 - Advent of Code 2025**

## Available Visualizations

### 1. **Simple Animation** (`animate_gui.py`)
Basic animated visualization that loops automatically.

```bash
cd animations
python animate_gui.py
```

**Features:**
- Automatic looping animation
- Color-coded display (green = protected, red = accessible)
- Shows each round of removal
- Clean, simple interface

**Speed:** 800ms between frames (hardcoded)

---

### 2. **Interactive Animation** (`animate_interactive.py`) ⭐ RECOMMENDED
Full-featured interactive visualization with controls.

```bash
cd animations
python animate_interactive.py
```

**Features:**
- ✅ Play/Pause button
- ✅ Reset button to restart
- ✅ Next button for frame-by-frame stepping
- ✅ Speed slider (0.1x to 2.0x speed)
- ✅ Frame counter
- ✅ Choose example or actual puzzle input

**Controls:**
- Click **Pause** to stop animation
- Click **Play** to resume
- Click **Reset** to go back to start
- Click **Next** to advance one frame manually
- Drag **Speed slider** to adjust playback speed
- Close window to exit

---

## Color Coding

All visualizations use consistent colors:

| Color | Meaning |
|-------|---------|
| 🟦 Dark Blue/Gray | Empty space (paper removed) |
| 🟢 Green | Paper roll (protected, has 4+ neighbors) |
| 🔴 Red | Accessible roll (will be removed next) |

---

## The Algorithm

1. **Find accessible rolls** - rolls with < 4 neighbors
2. **Remove them all simultaneously**
3. **Repeat** - some previously protected rolls may now be accessible
4. **Stop** when no more rolls are accessible

---

## Tips

- **For learning:** Use `animate_interactive.py` with Pause/Next to step through slowly
- **For small grids:** Example grid (10×10) is perfect for seeing details
- **For large puzzles:** The 139×139 grid is impressive but harder to see individual rolls
- **Save as GIF:** Edit `animate_gui.py` and uncomment the last line

---

## Requirements

```bash
# Already have these with NumPy
pip install numpy matplotlib
```

---

## Example Session

```bash
$ python animate_interactive.py

Select grid to visualize:
  1. Example grid (10x10)
  2. Your actual puzzle input

Enter choice (1 or 2): 1

Loading example grid...
Computing animation frames...

Animation ready!
  Total frames: 19
  Total rounds: 9

[Window opens with animation controls]
```

Use the buttons to control playback and watch the cascading removal effect!