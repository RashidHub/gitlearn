import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.rows * self.cell_size
        self.height = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        n = self.cell_size
        for i in range(0, self.height, self.cell_size):
            for j in range(0, self.width, self.cell_size):
                point1 = i // n
                point2 = j // n
                if self.life.curr_generation[point1][point2]:
                    pygame.draw.rect(self.screen, pygame.Color('green'),(j, i, n, n))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (j, i, n, n))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.life.create_grid(True)
        pause = False
        running = True
        while running and self.life.is_changing and \
                not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pause = not pause
                elif event.type == pygame.MOUSEBUTTONUP:
                    posx, posy = event.pos
                    posx //= self.cell_size
                    posy //= self.cell_size
                    self.life.curr_generation[posy][posx] = \
                        int(not bool(self.life.curr_generation[posy][posx]))
                    self.draw_grid()
                    pygame.display.flip()
            if pause:
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                continue
            self.draw_grid()
            self.draw_lines()
            self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
