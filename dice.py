import time
import random
import machine


def seed():
    """Find some source of randomness in the pico to seed the RNG"""

    seed = 0xFF * machine.ADC(4).read_u16() + time.time()


import picoscroll as scroll

# constants - layout of dice - all are in a 3x3 box so can encode as
# to binary byte strings

__DICE = (
    "000010000",
    "100000001",
    "100010001",
    "101000101",
    "101010101",
    "101101101",
)

__START = (
    "00000000000000000",
    "11100100110011110",
    "10010101001010000",
    "10010101000011100",
    "10010101001010000",
    "11100100110011110",
    "00000000000000000",
)

scroll.init()
width = scroll.get_width()
height = scroll.get_height()


def plot_die(die, x, y, b):
    """Write the digit at the offset starting at x, y with brightness b"""

    code = __DICE[die - 1]

    assert x >= 0
    assert x + 3 < width
    assert y >= 0
    assert y + 3 < height

    for _y in range(3):
        for _x in range(3):
            if code[_x + 3 * _y] == "1":
                scroll.set_pixel(_x + x, _y + y, b)
            else:
                scroll.set_pixel(_x + x, _y + y, 0)


def plot_dice(dice):
    """Plot all of the dice"""

    assert len(dice) <= 3
    assert all(die <= 6 and die >= 1 for die in dice)

    scroll.clear()
    for j, die in enumerate(dice):
        plot_die(die, width - 5 * (j + 1), 2, 16)

    scroll.update()


def start():
    """Display the word DICE"""

    seed()
    for y in range(7):
        for x in range(17):
            if __START[y][x] == "1":
                scroll.set_pixel(x, y, 16)
            else:
                scroll.set_pixel(x, y, 0)
    scroll.update()


def sparkle():
    """Some sparkling to make it look like a dice roll"""

    for n in range(random.randint(5, 10)):
        for j in range(width * height):
            y, x = divmod(j, width)
            b = 16 * ((n + j) % 2)
            scroll.set_pixel(x, y, b)
        scroll.update()
        time.sleep(0.1)


def roll():
    """Actually roll the dice"""

    dice = [random.randint(1, 6) for j in range(3)]
    plot_dice(dice)


def main():
    start()
    while True:
        time.sleep(0.1)
        if scroll.is_pressed(scroll.BUTTON_X):
            sparkle()
            roll()


main()
