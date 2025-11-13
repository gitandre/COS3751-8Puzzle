#!/usr/bin/env python3
import tkinter as tk
from collections import deque
import random
from typing import Tuple, List, Optional, Iterable

State = Tuple[int, ...]
GOAL: State = (1,2,3,4,5,6,7,8,0)

IX_TO_RC = [(i//3, i%3) for i in range(9)]
RC_TO_IX = {(r,c): r*3 + c for r in range(3) for c in range(3)}

def neighbors(s: State) -> Iterable[Tuple[State, str]]:
    zi = s.index(0); zr, zc = IX_TO_RC[zi]
    if zr > 0:  yield swap(s, zi, RC_TO_IX[(zr-1, zc)]), 'Up'
    if zr < 2:  yield swap(s, zi, RC_TO_IX[(zr+1, zc)]), 'Down'
    if zc > 0:  yield swap(s, zi, RC_TO_IX[(zr, zc-1)]), 'Left'
    if zc < 2:  yield swap(s, zi, RC_TO_IX[(zr, zc+1)]), 'Right'

def swap(s: State, i: int, j: int) -> State:
    lst = list(s); lst[i], lst[j] = lst[j], lst[i]; return tuple(lst)

def scramble(state: State, steps:int=20) -> State:
    s = state; last = None
    for _ in range(steps):
        opts = list(neighbors(s))
        if last is not None:
            opts = [o for o in opts if o[0] != last] or opts
        s, _ = random.choice(opts)
        last = s
    return s

def example_solution(start: State, goal: State) -> List[Tuple[State, Optional[str]]]:
    """
    Compute a shortest path from `start` to `goal` using Breadth-First Search (BFS).

    Returns:
        A list of (state, move) pairs:
            state : the puzzle configuration at that step
            move  : how we arrived there (Up/Down/Left/Right) — the first entry is None

        If no solution exists, returns an empty list.
    """

    print("=== BFS START ===")
    print(f"Start: {start}")
    print(f"Goal : {goal}")
    print("------------------")

    # If already solved, return trivial one-item path
    if start == goal:
        print("Start is already goal — trivial path.")
        return [(start, None)]

    # --- BFS Initialization ---

    # Frontier queue (FIFO) — BFS explores by increasing depth
    frontier = deque([start])

    # parent[state] = (previous_state, move_used_to_get_here)
    # start has no parent
    parent = {start: (None, None)}

    step = 0

    # --- BFS Search Loop ---
    while frontier:
        step += 1
        cur = frontier.popleft()

        print(f"\n>> STEP {step}")
        print(f"Expanding: {cur}")
        print(f"Frontier size before expansion: {len(frontier)+1}")

        # Stop if reached goal
        if cur == goal:
            print("Goal found! Stopping BFS.")
            break

        # Explore all neighbor states (children)
        for nxt, mv in neighbors(cur):
            if nxt not in parent:
                print(f"  Found new state via {mv}: {nxt}")
                parent[nxt] = (cur, mv)
                frontier.append(nxt)
            else:
                print(f"  Already visited: {nxt}")

        print(f"Frontier size after expansion: {len(frontier)}")

    # If the goal never appeared, no solution exists
    if goal not in parent:
        print("\nGoal NOT reachable — no solution.")
        print("=== BFS END ===")
        return []

    # --- Reconstruct path from goal → start using `parent` map ---
    print("\n=== RECONSTRUCTING PATH ===")
    path = []
    cur = goal
    depth = 0

    while cur is not None:
        prev_state, move_used = parent[cur]
        path.append((cur, move_used))
        print(f"  Step back {depth}: state={cur}, move_used={move_used}")
        cur = prev_state
        depth += 1

    # Reverse so path goes start → goal
    path.reverse()

    # First entry has no incoming move
    path[0] = (path[0][0], None)

    print("\n=== FINAL PATH ===")
    for i, (state, mv) in enumerate(path):
        print(f"  {i:2d}: move={mv}, state={state}")

    print("=== BFS END ===")
    return path



TILE, GAP = 110, 8
BOARD_W, BOARD_H = 3*TILE + 4*GAP, 3*TILE + 4*GAP
FONT = ("Helvetica", 30, "bold")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle Player (Fix)")
        # fixed size ensures canvas is visible
        self.geometry(f"{BOARD_W+40+200}x{BOARD_H+160}")

        self.start_state: State = GOAL
        self.current_state: State = GOAL
        self.solution: List[Tuple[State, Optional[str]]] = []
        self.idx = 0
        self.playing = False
        self.after_id = None
        self.speed_ms = 300

        top = tk.Frame(self); top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)
        tk.Button(top, text="Scramble", command=self.on_scramble).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="Reset",    command=self.on_reset).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="Load Example Solution", command=self.on_load_example).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="Step",     command=self.step).pack(side=tk.LEFT, padx=8)
        self.play_btn = tk.Button(top, text="Play", command=self.toggle_play)
        self.play_btn.pack(side=tk.LEFT, padx=4)

        # white canvas for maximum contrast
        self.canvas = tk.Canvas(self, width=BOARD_W, height=BOARD_H,
                                bg="white", highlightthickness=1, highlightbackground="#888")
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click_canvas)

        self.status = tk.Label(self, text="Ready")
        self.status.pack(side=tk.TOP, anchor="w", padx=12, pady=(0,8))

        # draw immediately and flush to the screen
        self.draw_board(self.current_state)
        self.update_idletasks()
        self.update()

    # ---- handlers ----
    def on_scramble(self):
        self.stop_play()
        self.start_state = scramble(GOAL, steps=18)
        self.current_state = self.start_state
        self.solution = []; self.idx = 0
        self.draw_board(self.current_state)
        self.status.config(text="Scrambled")

    def on_reset(self):
        self.stop_play()
        self.current_state = self.start_state
        self.idx = 0
        self.draw_board(self.current_state)
        self.status.config(text="Reset to start")

    def on_load_example(self):
        self.stop_play()
        self.solution = example_solution(self.start_state, GOAL)
        if not self.solution:
            self.status.config(text="No solution found by example BFS")
            return
        self.idx = 0
        self.draw_board(self.solution[0][0])
        self.status.config(text=f"Loaded solution ({len(self.solution)} states)")

    def toggle_play(self):
        if not self.solution:
            self.status.config(text="Load a solution first"); return
        if self.playing:
            self.stop_play()
        else:
            self.playing = True
            self.play_btn.config(text="Pause")
            self._tick()

    def stop_play(self):
        if self.after_id: self.after_cancel(self.after_id); self.after_id = None
        self.playing = False
        self.play_btn.config(text="Play")

    def _tick(self):
        if self.idx >= len(self.solution):
            self.stop_play(); self.status.config(text="Playback finished"); return
        state, mv = self.solution[self.idx]
        self.current_state = state
        self.draw_board(state, mv)
        self.status.config(text=f"Step {self.idx+1}/{len(self.solution)}  Move: {mv or '-'}")
        self.idx += 1
        if self.playing:
            self.after_id = self.after(self.speed_ms, self._tick)

    def step(self):
        self.stop_play()
        if not self.solution: self.status.config(text="Load a solution first"); return
        if self.idx >= len(self.solution): self.status.config(text="Success: GOAL !!! :)"); return
        state, mv = self.solution[self.idx]
        self.current_state = state
        self.draw_board(state, mv)
        self.idx += 1

    def on_click_canvas(self, e):
        # click-to-slide (manual move) for quick check the canvas is interactive
        x, y = e.x, e.y
        c, r = max(0, min(2, (x - GAP) // TILE)), max(0, min(2, (y - GAP) // TILE))
        idx = RC_TO_IX[(r, c)]
        zi = self.current_state.index(0); zr, zc = IX_TO_RC[zi]
        if abs(zr - r) + abs(zc - c) == 1:
            self.current_state = swap(self.current_state, zi, idx)
            self.draw_board(self.current_state)

    # ---- drawing ----
    def draw_board(self, state: Optional[State], highlight_move: Optional[str]=None):
        if state is None: state = GOAL
        self.canvas.delete("all")
        for r in range(3):
            for c in range(3):
                x0, y0 = GAP + c*TILE, GAP + r*TILE
                x1, y1 = x0 + TILE - GAP, y0 + TILE - GAP
                v = state[RC_TO_IX[(r,c)]]
                if v == 0:
                    self.canvas.create_rectangle(x0,y0,x1,y1, fill="#e8e8e8", outline="#bbb")
                else:
                    self.canvas.create_rectangle(x0,y0,x1,y1, fill="#f6f6f6", outline="#444", width=2)
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text=str(v),
                                            font=FONT, fill="#111")
        self.canvas.create_text(10, BOARD_H - 8, anchor="sw",
                                text=f"Move: {highlight_move or '-'}", fill="#333")

if __name__ == "__main__":
    App().mainloop()
