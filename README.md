# 8-Puzzle Player

A tiny GUI app to **play and solve the 8-puzzle**.
It uses **Breadth-First Search (BFS)** to compute a **shortest path** from a scrambled start to the goal.

---

## ✨ Features

* Visual 3×3 board with click-to-slide interaction
* **Scramble** the goal with a known-solvable sequence
* **Load Example Solution** (BFS shortest path) and **play** it step-by-step
* Adjustable playback speed (`speed_ms`)
* Clear, readable code: pure Python + Tkinter

---

## 🧱 State & Goal

* State is a 9-tuple of ints `0..8` in row-major order (0 = blank).
* Goal:

  ```python
  GOAL = (1,2,3,4,5,6,7,8,0)
  ```

---

## 📦 Requirements

* Python **3.8+**
* Tkinter (ships with most Python distributions; on Linux you may need `python3-tk`)

---

## 🚀 Run

Save the script (e.g., `eight_puzzle.py`) and run:

```bash
python3 eight_puzzle.py
```

---

## 🕹️ UI Controls

* **Scramble** — randomizes from the goal using legal moves only (keeps puzzle solvable)
* **Reset** — returns to the scrambled start
* **Load Example Solution** — runs **BFS** from current start to the `GOAL`
* **Step** — advance one move in the loaded solution
* **Play / Pause** — auto-play the loaded solution (`speed_ms` controls pace)
* **Click tiles** — click a tile adjacent to the blank to slide it manually

Status bar shows current step and last move.

---

## 🔎 How the Example Solver Works (BFS)

* Uses a **FIFO queue** and a `parent` map to reconstruct the path.
* Explores by **increasing depth** (each move = depth+1).
* Returns a list of `(state, move)` pairs from **start → goal**.
  The first entry has `move=None`.

Key pieces:

```python
def neighbors(s):  # legal moves from state s
def scramble(state, steps=20):  # random legal moves from GOAL
def example_solution(start, goal):  # BFS shortest path
```

> BFS prints a trace to the console (helpful for teaching/debugging).

---

## 🧩 Code Structure (high-level)

* **State helpers:** `IX_TO_RC`, `RC_TO_IX`, `swap`, `neighbors`
* **Puzzle ops:** `scramble(...)`
* **Solver:** `example_solution(...)` (BFS + parent pointers)
* **GUI:** `App(tk.Tk)` with a `Canvas` to draw the board

Tweak visuals at the top:

```python
TILE, GAP = 110, 8
FONT = ("Helvetica", 30, "bold")
# Playback speed (ms):
self.speed_ms = 300
```

---

## ✅ Solvability

`Scramble(GOAL, steps=N)` performs **N legal moves from the goal**, so the scrambled state is **always solvable**.

---

## 🛠️ Common Troubleshooting

* **Tkinter not found (Linux):** install `python3-tk`.
* **Window too large/small:** adjust `TILE` and `self.geometry(...)`.
* **Console too chatty:** comment out `print(...)` lines in `example_solution`.

---

## 🧠 Next Steps / Extensions

* Add **A*** with Manhattan distance `h(n)` and compare to BFS
* Add a **“Solve with A*”** button
* Show **move count** and **queue size** metrics
* Detect **already-at-goal** and short-circuit

---

## 📄 License

MIT (or choose your preferred license).

---

## 📬 Credits

* Built for teaching **uninformed search (BFS)** and GUI basics with Tkinter.
* The 8-puzzle is a classic from *Artificial Intelligence: A Modern Approach (AIMA)*.
