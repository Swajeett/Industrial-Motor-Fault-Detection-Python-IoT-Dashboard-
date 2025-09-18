# mcp3008.py
# MicroPython driver for MCP3008 ADC

class MCP3008:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cs.value(1)

    def read(self, channel):
        if channel < 0 or channel > 7:
            raise ValueError("Channel must be 0-7")

        self.cs.value(0)
        # Start bit (1), single-ended mode (1), channel bits
        cmd = 0x18 | channel
        buf = bytearray(3)
        buf[0] = 1
        buf[1] = cmd << 4
        buf[2] = 0

        self.spi.write_readinto(buf, buf)
        self.cs.value(1)

        # 10-bit result
        result = ((buf[1] & 3) << 8) | buf[2]
        return result
