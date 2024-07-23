import pygame

WIDTH = 550

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")

    for i in range(0,10):
        if(i%3 == 0):
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), ((50 + 50*i, 500)), 4)
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), ((500, 50 + 50*i)), 4)

        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), ((50 + 50*i, 500)), 2)
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), ((500, 50 + 50*i)), 2)
    pygame.display.update()