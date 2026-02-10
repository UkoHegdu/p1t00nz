# Ruutinju klade (means "Notebook", just the checkered one)
I am trying to build a numbers game that I used to play on paper while being bored in university. I don't remember who taught it to me. Anyway, credit to that guy (I'm 99% sure it was a guy).
Rules are in the help button when you play the game or in the code.
If I have time, I'll create this as an .exe as well, now I can't be bothered.

Run ciparinji.py to run the game.

#game #notebook #killingtime #boredinuniversity

---

## Game rules

**Goal:** Clear the board by removing every number. You win when the grid sum is 0.

**Board:** 3×9 grid. Initial layout:
```
1 2 3 4 5 6 7 8 9
1 1 1 2 1 3 1 4 1
5 1 6 1 7 1 8 1 9
```

**Removing numbers:** Click two cells. They are removed only if both conditions hold:
1. **Match:** The two values are either equal, or they sum to **10** (e.g. 3 and 7, 1 and 9).
2. **Adjacency:** In “reading order” (left-to-right, top-to-bottom), there must be no remaining (non-zero) number between the two cells. Same row: only zeros between them. Same column: only zeros between them. Different row and column: you can go from the first cell to the second along reading order (right to end of row, then next row, etc.) and every cell in between must be 0.

**Turns:** Pairs you remove in one “round” count as one turn until you use **Redraw**. **Redraw** packs all remaining numbers back into the grid in reading order (top-left, row by row), possibly adding new rows; using it starts a new turn. **Del empty** deletes rows that are fully empty (all zeros); using it increments the turn count.

**Difficulty:** **Easy** — you can press **Redraw** whenever you want. **Hard** — **Redraw** is only allowed when no valid pair exists (game checks via the same logic as the hint). Scores (turn count) are saved and shown on the scoreboard.

**Other:** **Hint** highlights one valid pair for a short time. You cannot select a cell that is already removed (value 0). Game over (lose) happens if Redraw would need more rows than the window can show.
