# GUI for the Sudoku game
import pygame
import time
from solver import solve, is_valid, find_empty
from sudoku_generator import generate_sudoku


class Grid:
  
    def __init__(self, rows, cols, width, height, win, board):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win, gap)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

       # Select the clicked cube
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def sketch(self, value):
        # Sketch the temporary number on the board
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            # Check if the inserted value is correct
            if is_valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def clear(self):
        # Remove the sketched in value
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        # Get the position of the click on the board
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def solve_gui(self):
        # Check if the board is already solved
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        # Insert numbers from 1 to 9 and check if it is valid
        for i in range(1,10):
            if is_valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()

                if self.solve_gui(): # Recursion
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()

        return False

class Cube:
    rows = 9
    cols = 9
    
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win, gap):
        x = self.col * gap
        y = self.row * gap

        # Draw the temporary value
        if self.temp != 0 and self.value == 0:
            font = pygame.font.SysFont("Arial", 25)
            text = font.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))

        # Draw the original value
        elif not(self.value == 0):
            font = pygame.font.SysFont("Arial", 35)
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        # Outline the selected cube
        if self.selected:
            pygame.draw.rect(win, (0,0,255), (x,y, gap ,gap), 3)

    def draw_change(self, win, is_correct):
        font = pygame.font.SysFont("Arial", 35)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if is_correct:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (0, 0, 255), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def format_time(secs):
    # Convert the time in seconds to a formatted string
    sec = secs % 60
    minute = (secs // 60) % 60
    hour = secs // 3600

    # Properly format the string with leading zeros if needed
    if hour > 0:
        formatted_time = f"{hour}:{minute:02}:{sec:02}"
    else:
        formatted_time = f"{minute:02}:{sec:02}"

    return formatted_time

def update_window(win, board, time, strikes):
    # Update the window with the current state of the board
    win.fill((255,255,255))
    left = 3 - strikes
    font = pygame.font.SysFont("Arial", 25)

    # Display time
    formatted_time = format_time(time)
    text = font.render("Time: " + formatted_time, 1, (0,0,0))
    win.blit(text, (10, 560))
    
    # Display Strikes
    if left == 1:
        strike_msg = font.render(str(left) + " strike left:", 1, (0, 0, 0))
    else:
        strike_msg = font.render(str(left) + " strikes left:", 1, (0, 0, 0))
    strike_count = font.render("X " * strikes, 1, (255, 0, 0))
    win.blit(strike_msg, (330, 560))
    win.blit(strike_count, (475, 560))

    board.draw()

def main():
    # Initialize the game window
    pygame.init()
    win = pygame.display.set_mode((550,600))
    pygame.display.set_caption("Sudoku")
    grid = generate_sudoku() # Generate a random sudoku puzzle
    board = Grid(9, 9, 550, 550, win, grid)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:

        play_time = round(time.time() - start)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if not board.place(board.cubes[i][j].temp):
                            strikes += 1
                        key = None
                
            # Check if the player has clicked on the board
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
            
        
        # Check if the player has selected a cube and pressed a key
        if board.selected and key != None:
            board.sketch(key)
            
        update_window(win, board, play_time, strikes)
        pygame.display.update()

        # Check if the player has lost
        if strikes == 3:
            print("Game over")
            board.solve_gui()


main()
pygame.quit()