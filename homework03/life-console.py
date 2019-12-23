import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    try:
                        screen.addstr(i + 1, j + 1, '*')
                    except curses.error:
                        pass
                else:
                    try:
                        screen.addstr(i + 1, j + 1, ' ')
                    except curses.error:
                        pass

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        self.draw_grid(screen)
        screen.refresh()
        time.sleep(1)
        while not self.life.is_max_generations_exceeded and self.life.is_changing:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(1)
        screen.clear()
        curses.endwin()