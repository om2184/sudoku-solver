# Sudoku solver using backtracking algorithm
from sudoku_generator import generate_sudoku
board = generate_sudoku()


def solve(board):
    # Check if the board is solved
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    # Insert numbers from 1 to 9 and check if it is valid
    for i in range (1,10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board): # Recursion
                return True
            
            board[row][col] = 0
        
    return False
    

def is_valid(board, number, position):
    
    # Check row
    for i in range (len(board[0])):
        if board[position[0]][i] == number and position[1] != i:
            return False
        
    # Check coloumn
    for i in range (len(board)):
        if board[i][position[1]] == number and position[0] != i:
            return False

    # Check box
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range (box_y * 3, box_y * 3 + 3):
        for j in range (box_x * 3, box_x * 3 + 3):
            if board[i][j] == number and (i,j) != position:
                return False
    
    return True
     
def find_empty(board):
    # Find the next empty cell
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    
    return None
