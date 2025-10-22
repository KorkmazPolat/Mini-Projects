# Rock-Paper-Scissors — Student-Style Single File

A simple Rock‑Paper‑Scissors project in one Python file. Includes a basic AI with a tiny conditional model and two ways to play:

- GUI: Buttons for Rock/Paper/Scissors and an analytics panel
- CLI: Type r/p/s and see analytics printed after each round

The AI keeps small counts keyed by the last two rounds (result + AI’s last move) and tries to predict your next move from that context. If no data exists, it falls back to a uniform guess.

## Requirements

- Python 3.8+
- Tkinter for GUI (usually included with Python on macOS/Windows). If Tkinter isn’t available, use CLI mode.

## Run

- GUI mode:
  `python Rock-Paper-Scissors-MiniProject/play.py --mode gui`

- CLI mode:
  `python Rock-Paper-Scissors-MiniProject/play.py --mode cli`

## Notes

- After each round, analytics show:
  - Which context was used (last two rounds)
  - Raw counts and normalized distribution for your predicted move
  - The predicted move and the AI’s chosen counter-move

