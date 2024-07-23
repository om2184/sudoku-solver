import pygame
from solver import solve, isValid, findEmpty


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

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def sketch(self, value):
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if isValid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None


    def solve_gui(self):
        find = findEmpty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if isValid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()

                if self.solve_gui():
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

        if self.temp != 0 and self.value == 0:
            font = pygame.font.SysFont("Arial", 25)
            text = font.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            font = pygame.font.SysFont("Arial", 35)
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (0,0,255), (x,y, gap ,gap), 3)

    
    def draw_change(self, win, is_correct):
        fnt = pygame.font.SysFont("Arial", 35)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if is_correct:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (0, 0, 255), (x, y, gap, gap), 3)




    
    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val



def main():
    pygame.init()
    win = pygame.display.set_mode((550,600))
    pygame.display.set_caption("Sudoku")
    grid = [
        [0, 5, 8, 0, 0, 9, 0, 1, 0],
        [0, 0, 3, 0, 6, 2, 0, 0, 0],
        [0, 9, 1, 0, 3, 8, 0, 0, 0],
        [0, 8, 0, 0, 0, 3, 0, 0, 7],
        [3, 0, 4, 0, 0, 0, 0, 0, 5],
        [0, 7, 9, 0, 5, 4, 0, 0, 0],
        [9, 6, 2, 3, 0, 5, 7, 8, 0],
        [0, 1, 0, 0, 0, 6, 0, 3, 9],
        [4, 3, 0, 8, 9, 0, 5, 2, 0]
    ]
    board = Grid(9, 9, 550, 550, win, grid)
    key = None
    run = True

    while run:
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
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                        key = None

                        if board.is_finished():
                            print("Game over")

                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
            
            if board.selected and key != None:
                board.sketch(key)
            
            win.fill((255,255,255))
            board.draw()
            pygame.display.update()

main()
pygame.quit()