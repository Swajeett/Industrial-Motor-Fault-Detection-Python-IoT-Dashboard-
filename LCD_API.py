# lcd_api.py
# Generic LCD API for MicroPython

import time

class LcdApi:
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_ENTRY_INC = 0x02
    LCD_ENTRY_SHIFT = 0x01
    LCD_ON_CTRL = 0x08
    LCD_ON_DISPLAY = 0x04
    LCD_ON_CURSOR = 0x02
    LCD_ON_BLINK = 0x01
    LCD_MOVE = 0x10
    LCD_MOVE_DISP = 0x08
    LCD_MOVE_RIGHT = 0x04
    LCD_FUNCTION = 0x20
    LCD_FUNCTION_8BIT = 0x10
    LCD_FUNCTION_2LINES = 0x08
    LCD_FUNCTION_10DOTS = 0x04
    LCD_CGRAM = 0x40
    LCD_DDRAM = 0x80
    LCD_ROW_OFFSETS = [0x00, 0x40, 0x14, 0x54]

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        if self.num_lines > 4:
            self.num_lines = 4
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self.init_lcd()

    def init_lcd(self):
        raise NotImplementedError

    def clear(self):
        self.write_cmd(self.LCD_CLR)
        self.cursor_x = 0
        self.cursor_y = 0
        time.sleep_ms(2)

    def home(self):
        self.write_cmd(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y = 0
        time.sleep_ms(2)

    def move_to(self, col, row):
        self.cursor_x = col
        self.cursor_y = row
        addr = self.LCD_DDRAM | (col + self.LCD_ROW_OFFSETS[row])
        self.write_cmd(addr)

    def putchar(self, char):
        self.write_data(ord(char))

    def putstr(self, string):
        for char in string:
            self.putchar(char)
