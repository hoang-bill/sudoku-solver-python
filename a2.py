#!/usr/bin/python3
# B351/Q351 Fall 2024
# Do not share these assignments or their solutions outside of this class.

import csv
import itertools

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        # initialize all of the variables
        self.n2 = 0 # legnth of one side of the board
        self.n = 0 # length of one side of an inner square
        self.spaces = 0 # total number of cells in Sudoku board (81 total)
        self.board = None # mapping dictionary
        self.valsInRows = None # mapping values to rowIndex
        self.valsInCols = None # mapping values to columnIndex
        self.valsInBoxes = None # mapping inner box index to value
        self.unsolvedSpaces = None # represents squares on the board that are empty (represented with a 0)

        # load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    # loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                # Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valsInRows = [set() for _ in range(self.n2)]
                        self.valsInCols = [set() for _ in range(self.n2)]
                        self.valsInBoxes = [set() for _ in range(self.n2)]
                        self.unsolvedSpaces = set(itertools.product(range(self.n2), range(self.n2)))

                # check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row must have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                # add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valsInRows[reader.line_num-1].add(int(item))
                        self.valsInCols[index].add(int(item))
                        self.valsInBoxes[self.spaceToBox(reader.line_num-1, index)].add(int(item))
                        self.unsolvedSpaces.remove((reader.line_num-1, index))


    ##########################################
    ####   Utility Functions
    ##########################################

    # converts a given row and column to its inner box number
    def spaceToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n

    # prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            # add row divider
            if r % self.n == 0 and not r == 0:
                if self.n2 > 9:
                    print("  " + "----" * self.n2)
                else:
                    print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                # add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                # add value placeholder
                if self.n2 > 9:
                    if val is None: row += "__"
                    else: row += "%2i" % val
                else:
                    if val is None: row += "_"
                    else: row += str(val)
            print(row)


    ##########################################
    ####   Move Functions - YOUR IMPLEMENTATIONS GO HERE
    ##########################################

    # makes a move, records it in its row, col, and box, and removes the space from unsolvedSpaces
    def makeMove(self, space, value):
        # Assign value to the space in the board
        self.board[space] = value

        # Record that the value has occurred in the row, column and box of the space 
        self.valsInRows[space[0]].add(value)  
        self.valsInCols[space[1]].add(value)
        self.valsInBoxes[self.spaceToBox(space[0], space[1])].add(value)

        # Remove the space from the set of unsolved spaces
        self.unsolvedSpaces.remove(space)

    # removes the move, its record in its row, col, and box, and adds the space back to unsolvedSpaces
    def undoMove(self, space, value):
        # Delete the space from the board
        del self.board[space]

        # Record that the value no longer appears in the row, column and box of the space
        self.valsInRows[space[0]].remove(value)
        self.valsInCols[space[1]].remove(value)
        self.valsInBoxes[self.spaceToBox(space[0], space[1])].remove(value)

        # Add the space to the set of unsolved spaces 
        self.unsolvedSpaces.add(space)

    # returns True if the space is empty and on the board,
    # and assigning value to it if not blocked by any constraints
    def isValidMove(self, space, value):
        # Return False if the space is not on the board
        if space not in itertools.product(range(self.n2), range(self.n2)):
            return False
        
        # Return False if the space is not empty  
        if space in self.board:
            return False
        
        # Check if the value has not already occurred in the column, row and box of the space
        if (value in self.valsInRows[space[0]] or
            value in self.valsInCols[space[1]] or 
            value in self.valsInBoxes[self.spaceToBox(space[0], space[1])]):
            return False
        
        # Return True as the assignment is valid
        return True

    # optional helper function for use by getMostConstrainedUnsolvedSpace
    def evaluateSpace(self, space):
        # Return the number of values already used in the space's row, column and box
        return (len(self.valsInRows[space[0]]) + 
                len(self.valsInCols[space[1]]) +
                len(self.valsInBoxes[self.spaceToBox(space[0], space[1])]))

    # gets the unsolved space with the most current constraints
    # returns None if unsolvedSpaces is empty
    def getMostConstrainedUnsolvedSpace(self):
        # Return None if the board is fully solved
        if not self.unsolvedSpaces:
            return None
        
        # Find the unsolved space with maximum number of constraints
        return max(self.unsolvedSpaces, key=self.evaluateSpace)

class Solver:
    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self):
        pass

    ##########################################
    ####   Solver
    ##########################################

    # recursively selects the most constrained unsolved space and attempts
    # to assign a value to it

    # upon completion, it will leave the board in the solved state (or original
    # state if a solution does not exist)

    # returns True if a solution exists and False if one does not
    def solveBoard(self, board):
        # Get the most constrained unsolved space on the board
        space = board.getMostConstrainedUnsolvedSpace()
        
        # Return True if board is already solved
        if space is None:
            return True

        # Try assigning each possible value to the space
        for value in range(1, board.n2 + 1):
            # If the value is valid, make the move and recursively solve the board
            if board.isValidMove(space, value):
                board.makeMove(space, value)
                if self.solveBoard(board):
                    return True
                    
                # Undo the move if it does not lead to a solution
                board.undoMove(space, value)
                
        # Return False if no solution exists for the board
        return False


if __name__ == "__main__":
    # change this to the input file that you'd like to test
    board = Board('/Users/billhoang/Library/CloudStorage/OneDrive-IndianaUniversity/FA\'24/CSCI-C 351 - Intro to Artificial Intelligence/Assignment/2P/tests/test-3-hard/10.csv')
    s = Solver()
    s.solveBoard(board)
    board.print()
