from dokusan import generators
import numpy as np
import random
def generate_sudoku():
    arr = np.array(list(str(generators.random_sudoku(avg_rank=100))))
    arr1 = arr.astype(int).reshape(9,9)
    return arr1

