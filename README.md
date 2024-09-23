# Sudoku Solver

This repository contains a Python implementation of a Sudoku solver that utilizes backtracking search with forward checking (constraint propagation) to solve Sudoku puzzles of various difficulties.

## Background

Sudoku is a popular puzzle game where the objective is to fill a 9x9 grid with digits so that each column, each row, and each of the nine 3x3 subgrids contains all of the digits from 1 to 9. The puzzle setter provides a partially completed grid, and the challenge is to solve the puzzle by filling in the empty cells.

## Features

- Solves Sudoku puzzles of various sizes (n^2 x n^2)
- Implements backtracking search with forward checking for efficient solving
- Supports input of Sudoku puzzles via CSV files
- Provides a command-line interface to display the solved puzzle

## Requirements

- Python 3.x

## Installation

1. Clone the repository: git clone https://github.com/your-username/sudoku-solver.git
2. Navigate to the project directory: cd sudoku-solver

## Usage

1. Prepare your Sudoku puzzle in a CSV file format, where empty cells are represented by empty strings. Place the CSV file in the `tests` directory.

2. Open the `sudoku-solver.py` file and modify the `if __name__ == "__main__":` block at the bottom of the script to specify the path to your CSV file:

```python
if __name__ == "__main__":
    board = Board('tests/your-puzzle.csv')
    s = Solver()
    s.solveBoard(board)
    board.print()
