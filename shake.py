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
class ShakeApplication:
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

    def __update_blocks(self):
        for i, block in enumerate(self.blocks):
            if block.life == self.length:
                del self.blocks[i]
                continue
            block.life += 1

    def __draw_blocks(self):
        for block in self.blocks:
            self.stdscr.addstr(block.y, block.x, self.character_avatar)

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
        self.stdscr.addstr(self.apple.y, self.apple.x, self.apple_avatar)

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

    def start(self):
        # Clear screen
        stdscr = self.stdscr
        stdscr.clear()
        self.__generate_apple()

        self.length = 1
        self.elements = [ShakeBlock(self.x, self.y)]

        curses.halfdelay(self.delay)
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
                return -1
            self.blocks.append(ShakeBlock(self.x, self.y))
            stdscr.clear()

            if self.x == self.apple.x and self.y == self.apple.y:
                self.length += 1
                self.__generate_apple()
            self.__update_blocks()
            self.__draw_apple()
            self.__draw_blocks()
            # stdscr.addstr(self.y, self.x, self.character_avatar)
            stdscr.refresh()

        stdscr.refresh()
        stdscr.getkey()


if __name__ == "__main__":
    app = ShakeApplication()
    app.start()
