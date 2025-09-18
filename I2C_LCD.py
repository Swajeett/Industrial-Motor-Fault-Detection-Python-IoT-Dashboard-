# i2c_lcd.py
# I2C LCD driver for MicroPython

from lcd_api import LcdApi
import time
from machine import I2C

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = 0x08
        self.init_lcd()

    def hal_write_init_nibble(self, nibble):
        byte = (nibble << 4) | self.backlight
        self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
        time.sleep_us(500)
        self.i2c.writeto(self.i2c_addr, bytearray([byte & ~0x04]))
        time.sleep_us(100)

    def hal_backlight_on(self):
        self.backlight = 0x08
        self.i2c.writeto(self.i2c_addr, bytearray([self.backlight]))

    def hal_backlight_off(self):
        self.backlight = 0x00
        self.i2c.writeto(self.i2c_addr, bytearray([self.backlight]))

    def write_cmd(self, cmd):
        self.hal_write_byte(cmd, False)

    def write_data(self, data):
        self.hal_write_byte(data, True)

    def hal_write_byte(self, data, char_mode):
        upper = data & 0xF0
        lower = (data << 4) & 0xF0
        self.hal_write_nibble(upper, char_mode)
        self.hal_write_nibble(lower, char_mode)

    def hal_write_nibble(self, nibble, char_mode):
        byte = nibble | self.backlight
        if char_mode:
            byte |= 0x01
        self.i2c.writeto(self.i2c_addr, bytearray([byte | 0x04]))
        time.sleep_us(500)
        self.i2c.writeto(self.i2c_addr, bytearray([byte & ~0x04]))
        time.sleep_us(100)
