import pygame
import random

from pygame.locals import *
from typing import List, Tuple
from copy import deepcopy


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.grid = self.create_grid(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.get_next_generation()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

    def create_grid(self, randomize: bool=False) -> Grid:
        grid = [[random.randint(0,1) for y in range(self.cell_width)] for x in range(self.cell_height)]
        if randomize:
            pass
        else:
            grid = [[0 for y in range(self.cell_width)] for x in range(self.cell_height)]
        return grid

    def draw_grid(self) -> None:
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                    (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size))
                elif self.grid[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                    (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []

        for i in range(max(0, row - 1), min(self.cell_height, row + 2)):
            for j in range(max(0, col - 1), min(self.cell_width, col + 2)):
                if i == row and j == col:
                    continue
                neighbours.append(self.grid[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = deepcopy(self.grid)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j]:
                    if sum(self.get_neighbours((i, j))) in (2, 3):
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if sum(self.get_neighbours((i, j))) == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
        self.grid = new_grid
        return self.grid

if __name__ == '__main__':
    game = GameOfLife(320, 240, 10)
    game.run()