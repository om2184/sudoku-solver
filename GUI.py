import pygame
import requests

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
grid_original = [[grid[x][y] for y in range (len(grid[0]))] for x in range (len(grid))]

WIDTH = 550
background_colour = (255, 255, 255)
original_grid_colour = (52, 35, 151)


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_colour)
    myfont = pygame.font.SysFont("Comic Sans MS", 35)

    for i in range(0,10):
        if(i%3 == 0):
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), ((50 + 50*i, 500)), 4)
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), ((500, 50 + 50*i)), 4)

        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), ((50 + 50*i, 500)), 2)
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), ((500, 50 + 50*i)), 2)
    pygame.display.update()

    for i in range (0, len(grid[0])):
        for j in range (0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, original_grid_colour)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
    
main()