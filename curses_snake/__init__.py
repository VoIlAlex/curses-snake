import curses
import random
import time
from cursy import curses_application


class ShakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 0


class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y


@curses_application
class SnakeApplication:
    def __init__(self):
        self.delay = 1
        self.x = 0
        self.y = 0
        self.direction = 'r'
        self.character_avatar = '*'
        self.apple_avatar = '◯'
        self.length = 0
        self.blocks = []
        self.apple = None

        # Game over stuff
        self.current_color_idx = 0
        self.colors_number = 0
        self.is_playing = False

    def __reset_game(self):
        self.length = 1
        self.blocks = [ShakeBlock(self.x, self.y)]
        self.direction = 'r'
        self.x = 0
        self.y = 0
        self.delay = 1
        self.apple = None
        self.current_color_idx = 0

    def __update_blocks(self):
        for i, block in enumerate(self.blocks):
            if block.life == self.length:
                del self.blocks[i]
                continue
            block.life += 1

    def __draw_blocks(self):
        for block in self.blocks:
            try:
                self.stdscr.addch(block.y, block.x, self.character_avatar)
            except curses.error:
                continue

    def __is_tail_touched(self):
        for block in self.blocks:
            if block.x == self.x and block.y == self.y:
                return True
        return False

    def __generate_apple(self):
        height, width = self.stdscr.getmaxyx()
        self.apple = Apple(
            x=random.randint(0, width - 1),
            y=random.randint(0, height - 1)
        )

    def __draw_apple(self):
        self.stdscr.addch(self.apple.y, self.apple.x, self.apple_avatar)

    def __draw_game_over(self):
        height, width = self.stdscr.getmaxyx()
        game_over = 'GAME OVER'
        self.stdscr.addstr(height // 2, width // 2 -
                           len(game_over),
                           game_over,
                           curses.A_BOLD | curses.color_pair(self.current_color_idx))
        self.current_color_idx = (
            self.current_color_idx + 1
        ) % self.colors_number

    def __update_direction(self, ch):
        if ch != -1:
            ch = chr(ch)
            if ch == 'h' and self.direction != 'r':
                self.direction = 'l'
            elif ch == 'l' and self.direction != 'l':
                self.direction = 'r'
            elif ch == 'j' and self.direction != 'u':
                self.direction = 'd'
            elif ch == 'k' and self.direction != 'd':
                self.direction = 'u'

    def __init_color(self, foreground, background=curses.COLOR_BLACK):
        curses.init_pair(self.colors_number, foreground, background)
        self.colors_number += 1

    def __setup_curses(self):
        curses.start_color()
        curses.use_default_colors()
        self.__init_color(curses.COLOR_RED)
        self.__init_color(curses.COLOR_GREEN)
        self.__init_color(curses.COLOR_MAGENTA)
        self.__init_color(curses.COLOR_YELLOW)

    def start(self):
        self.is_playing = True
        # Clear screen
        stdscr = self.stdscr
        stdscr.clear()
        self.__reset_game()
        self.__setup_curses()
        self.__generate_apple()

        curses.halfdelay(self.delay)
        ch = -1
        while True:

            height, width = stdscr.getmaxyx()
            ch = stdscr.getch()
            self.__update_direction(ch)

            if ch == 259:
                self.delay = self.delay - 1 if self.delay > 1 else 1
            elif ch == 258:
                self.delay = self.delay + 1

            if self.direction == 'r':
                curses.halfdelay(self.delay)
                if self.x >= width - 1:
                    self.x = 0
                else:
                    self.x += 1
            elif self.direction == 'l':
                curses.halfdelay(self.delay)
                if self.x != 0:
                    self.x -= 1
                else:
                    self.x = width - 1
            elif self.direction == 'u':
                curses.halfdelay(self.delay * 2)
                if self.y != 0:
                    self.y -= 1
                else:
                    self.y = height - 1
            elif self.direction == 'd':
                curses.halfdelay(self.delay * 2)
                if self.y >= height - 1:
                    self.y = 0
                else:
                    self.y += 1

            if self.__is_tail_touched():
                self.is_playing = False
                curses.halfdelay(5)
                while True:
                    self.stdscr.clear()
                    self.__draw_game_over()
                    ch = self.stdscr.getch()
                    if ch != -1:
                        break
                self.__reset_game()
                self.__generate_apple()
                continue
            self.blocks.append(ShakeBlock(self.x, self.y))
            stdscr.clear()

            # Quit the game
            if ch != -1 and chr(ch) == 'q':
                return

            if self.x == self.apple.x and self.y == self.apple.y:
                self.length += 1
                self.__generate_apple()
            self.__update_blocks()
            try:
                self.__draw_apple()
            except:
                self.__generate_apple()
            finally:
                self.__draw_apple()
            self.__draw_blocks()
            # stdscr.addstr(self.y, self.x, self.character_avatar)
            stdscr.refresh()

        stdscr.refresh()
        stdscr.getkey()
        self.is_playing = False
