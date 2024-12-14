2048 Python with AI
===================

[![Run on Repl.it](https://repl.it/badge/github/yangshun/2048-python)](https://repl.it/github/yangshun/2048-python)

---

This project is a Python implementation of the popular game [2048](https://github.com/gabrielecirulli/2048) by Gabriele Cirulli. The objective of the game is to slide numbered tiles on a grid to combine them to create a tile with the number 2048. This version uses TKinter for the graphical interface and includes several AI strategies to play the game.

![screenshot](img/screenshot.png)

## Getting Started

To start the game, run:

    $ python3 puzzle.py

## AI Implementations

This project includes several AI strategies to play the game:

1. **Greedy AI**: Selects the move that maximizes a heuristic value.
2. **Expectimax AI**: Uses the expectimax algorithm to choose the best move.
3. **Monte Carlo Tree Search (MCTS) AI**: Uses MCTS to simulate and select the best move.

### Running the AIs

To run the Greedy AI:

    $ python3 greedy_ai.py

To run the Expectimax AI:

    $ python3 expectimax_ai.py

To run the MCTS AI:

    $ python3 mcts_ai.py

## Heuristics

Several heuristics are implemented to evaluate the board state:

- **Score Heuristic**: Sum of all tile values.
- **Open Cells Heuristic**: Number of empty cells.
- **Max Tile Heuristic**: Value of the highest tile.
- **Tile Sum Heuristic**: Weighted sum of all tile values.

## Contributors

- [Yanghun Tay](http://github.com/yangshun)
- [Emmanuel Goh](http://github.com/emman27)

