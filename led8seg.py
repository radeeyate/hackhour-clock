import board
import digitalio
import time
from busio import SPI

# constants for digit selection
KILOBIT = 0xFE
HUNDREDS = 0xFD
TENS = 0xFB
UNITS = 0xF7
Dot = 0x80

# 7-segment display encoding for hex digits
SEG8Code = [
    0x3F,  # 0
    0x06,  # 1
    0x5B,  # 2
    0x4F,  # 3
    0x66,  # 4
    0x6D,  # 5
    0x7D,  # 6
    0x07,  # 7
    0x7F,  # 8
    0x6F,  # 9
    0x77,  # A
    0x7C,  # b
    0x39,  # C
    0x5E,  # d
    0x79,  # E
    0x71,  # F
]


class LED_8SEG:
    def __init__(self, mosi_pin=board.GP11, sck_pin=board.GP10, rclk_pin=board.GP9):
        self.rclk = digitalio.DigitalInOut(rclk_pin)
        self.rclk.direction = digitalio.Direction.OUTPUT
        self.rclk.value = True

        self.spi = SPI(sck_pin, mosi_pin)  # create SPI object
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=10000000)  # configure SPI
        self.spi.unlock()
        self.SEG8 = SEG8Code

    def write_cmd(self, num, seg):
        self.rclk.value = True
        while not self.spi.try_lock():  # acquire the SPI bus lock
            pass
        self.spi.write(bytearray([num]))
        self.spi.write(bytearray([seg]))
        self.spi.unlock()  # release the lock after usage
        self.rclk.value = False
        time.sleep(0.002)
        self.rclk.value = True

    def clear_display(self):
        self.write_cmd(UNITS, 0x00)
        self.write_cmd(TENS, 0x00)
        self.write_cmd(HUNDREDS, 0x00)
        self.write_cmd(KILOBIT, 0x00)

    def display_number(self, number):
        self.clear_display()
        time.sleep(0.002)
        self.write_cmd(UNITS, self.SEG8[number % 10])
        time.sleep(0.002)
        self.write_cmd(TENS, self.SEG8[(number % 100) // 10])
        time.sleep(0.002)
        self.write_cmd(HUNDREDS, self.SEG8[(number % 1000) // 100] | Dot)
        time.sleep(0.002)
        self.write_cmd(KILOBIT, self.SEG8[(number % 10000) // 1000])
