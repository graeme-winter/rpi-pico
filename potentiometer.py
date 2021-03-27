import time
import machine

import picoscroll as scroll

# constants - layout of numbers - all are in a 4x5 box so can encode as
# to binary byte strings

__NUMBERS = (
    "01101011110110010110",
    "00100110001000100010",
    "01101001001001001111",
    "11100001001000011110",
    "10011001111100010001",
    "11111000111000011110",
    "01101000111010010110",
    "11110001001000100010",
    "01101001011010010110",
    "01101001011100010110",
)

scroll.init()
width = scroll.get_width()
height = scroll.get_height()
pot = machine.ADC(26)


def plot_digit(digit, x, y, b):
    """Write the digit at the offset starting at x, y with brightness b"""

    code = __NUMBERS[digit]

    assert x >= 0
    assert x + 4 < width
    assert y >= 0
    assert y + 5 < height

    for _y in range(5):
        for _x in range(4):
            if code[_x + 4 * _y] == "1":
                scroll.set_pixel(_x + x, _y + y, b)
            else:
                scroll.set_pixel(_x + x, _y + y, 0)


def plot_number(value):
    assert value < 1000
    digits = map(int, reversed(str(value)))
    scroll.clear()
    for j, digit in enumerate(digits):
        plot_digit(digit, width - 5 * (j + 1), 1, 64)
    scroll.update()


while True:
    r = int(round(100 * pot.read_u16() / 65535.0))
    plot_number(r)
    time.sleep(0.2)
