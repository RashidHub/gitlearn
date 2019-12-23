import pathlib
import random

from typing import List, Optional, Tuple
from copy import deepcopy

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]

class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        Grid = [[random.randint(0, 1) for y in range(self.cols)] for x in range(self.rows)]
        if randomize:
            pass
        else:
            Grid = [[0 for y in range(self.cols)] for x in range(self.rows)]
        return Grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []

        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if i == row and j == col:
                    continue
                neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j]:
                    if sum(self.get_neighbours((i, j))) in (2, 3):
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if sum(self.get_neighbours((i, j))) == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
        return new_grid

    def step(self) -> None:
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        grid = []
        string_grid = filename.read_text().split('\n')
        rows = len(string_grid)
        cols = len(string_grid[0])
        string_grid = string_grid[:-1]
        for i in string_grid:
            arr = []
            for elem in i:
                arr.append(int(elem))
            grid.append(arr)
        game = GameOfLife((rows, cols), False)
        game.curr_generation = copy.deepcopy(grid)
        return game

    def save(filename: pathlib.Path) -> None:
        for i in self.curr_generation:
            for elem in i:
                filename.write_text(str(elem).replace("'", ''))
            filename.write_text('\n')