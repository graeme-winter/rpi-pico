# rowcounter.py
#
# Counter for counting rows when knitting, which includes a time indicator
# which counts for ~ 250s since count was last changed, to answer the
# question "did I just count that row?"
#
# (C) Graeme Winter, 2021
#
# UI:
#
# A                  X
# +------------------+
# |                  |
# +------------------+
# B                  Y
#
# A: reset
# X: increment counter
# Y: decrement counter
# B+X: increase counter brightness
# B+Y: decrease counter brightness
#

import time

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
__WIDTH = scroll.get_width()
__HEIGHT = scroll.get_height()
__INI = "count.ini"

t0 = time.time()
count = 0
brightness = 8


def load():
    try:
        global count
        count = int(open(__INI, "r").read())
        if count < 0:
            count = 0
    except:
        count = 0


def save():
    with open(__INI, "w") as f:
        f.write(str(count))


def plot_digit(digit, x, y, b):
    """Write the digit at the offset starting at x, y with brightness b"""

    code = __NUMBERS[digit]

    assert x >= 0
    assert x + 4 <= __WIDTH
    assert y >= 0
    assert y + 5 <= __HEIGHT

    for _y in range(5):
        for _x in range(4):
            if code[_x + 4 * _y] == "1":
                scroll.set_pixel(_x + x, _y + y, b)
            else:
                scroll.set_pixel(_x + x, _y + y, 0)


def plot_time():
    """Plot the time as a bar across the top - last pip will blink"""
    dt = time.time() - t0
    n = dt // 10 + 1
    if n > 25:
        n = 25
    for j in range(n):
        y, x = divmod(j, 5)
        if j == n - 1 and dt % 2:
            scroll.set_pixel(x + 1, y + 1, brightness)
        else:
            scroll.set_pixel(x + 1, y + 1, brightness // 2)
    for j in range(n, 25):
        y, x = divmod(j, 5)
        scroll.set_pixel(x + 1, y + 1, 0)


def plot_count():
    """Write the right-justified count"""
    assert count < 1000
    digits = map(int, reversed(str(count)))
    scroll.clear()
    for j, digit in enumerate(digits):
        plot_digit(digit, __WIDTH - 5 * (j + 1), 1, brightness)


def update():
    plot_time()
    scroll.update()


def main():
    global t0, count, brightness
    load()
    plot_count()
    while True:
        # dumb switch debouncing - time.sleep(0.1) below
        x = scroll.is_pressed(scroll.BUTTON_X)
        y = scroll.is_pressed(scroll.BUTTON_Y)
        a = scroll.is_pressed(scroll.BUTTON_A)
        b = scroll.is_pressed(scroll.BUTTON_B)

        if b and x:
            if brightness < 128:
                brightness *= 2
            plot_count()
            update()
            time.sleep(0.25)

        elif x:
            count += 1
            t0 = time.time()
            save()
            plot_count()
            update()
            time.sleep(0.25)

        if b and y:
            if brightness > 1:
                brightness //= 2
            plot_count()
            update()
            time.sleep(0.25)

        elif y and count > 0:
            count -= 1
            t0 = time.time()
            save()
            plot_count()
            update()
            time.sleep(0.25)

        if a:
            count = 0
            t0 = time.time()
            plot_count()
            save()

        update()
        time.sleep(0.02)


main()
