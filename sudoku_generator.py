# Generate a random sudoku puzzle
from dokusan import generators
import numpy as np

def generate_sudoku():
    generated = np.array(list(str(generators.random_sudoku(avg_rank=100))))
    
    # Convert the string to a 9x9 numpy integer array
    formated = generated.astype(int).reshape(9,9)
    return formated

