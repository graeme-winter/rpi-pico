# Counter for counting rows when knitting, which includes a time indicator
# which counts for ~ 12 minutes since count was last changed, to answer the
# question "did I just count that row?"
#
# (C) Graeme Winter, 2021
#
# UI:
#
# Y                  B
# +------------------+
# |                  |======
# +------------------+
# X                  A
#
# Y: reset
# X: toggle A / B counter
# B: increment counter
# A: decrement counter

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
count_a = 0
count_b = 0
brightness = 8

# which one are we showing? a or b? if +1, a; -1, b
showing = 1


def load():
    try:
        global count_a, count_b, showing
        saved = int(open(__INI, "r").read())
        if saved < 0:
            count_a = saved % 1000
            count_b = saved // 1000
            showing = -1
        else:
            count_a = saved % 1000
            count_b = saved // 1000
            showing = 1

    except:
        count_a = 0
        count_b = 0
        showing = 1


def save():
    with open(__INI, "w") as f:
        save = 1000 * count_b + count_a
        f.write(str(showing * save))


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
                scroll.set_pixel(16 - (_x + x), 6 - (_y + y), b)
            else:
                scroll.set_pixel(16 - (_x + x), 6 - (_y + y), 0)


def plot_time():
    """Plot the time as a bar across the top - last pip will blink"""
    dt = time.time() - t0
    n = dt // 30 + 1
    if n > 25:
        n = 25
    for j in range(n):
        y, x = divmod(j, 5)
        if j == n - 1 and dt % 2:
            scroll.set_pixel(16 - (x + 1), 6 - (y + 1), brightness)
        else:
            scroll.set_pixel(16 - (x + 1), 6 - (y + 1), brightness // 2)
    for j in range(n, 25):
        y, x = divmod(j, 5)
        scroll.set_pixel(16 - (x + 1), 6 - (y + 1), 0)


def plot_count():
    """Write the right-justified count"""
    scroll.clear()
    if showing > 0:
        count = count_a
        for j in 4, 5, 6:
            scroll.set_pixel(16, j, brightness)
    else:
        count = count_b
        for j in 0, 1, 2:
            scroll.set_pixel(16, j, brightness)
    assert count < 1000
    digits = map(int, reversed(str(count)))
    for j, digit in enumerate(digits):
        plot_digit(digit, __WIDTH - 5 * (j + 1), 1, brightness)


def update():
    plot_time()
    scroll.update()


def incr_count():
    global count_a, count_b, showing
    if showing > 0:
        count_a += 1
    else:
        count_b += 1


def decr_count():
    global count_a, count_b, showing
    if showing > 0:
        if count_a > 0:
            count_a -= 1
    else:
        if count_b > 0:
            count_b -= 1


def zero_count():
    global count_a, count_b, showing
    if showing > 0:
        count_a = 0
    else:
        count_b = 0


def main():
    global t0, count_a, count_b, showing, brightness
    load()
    plot_count()
    while True:
        # dumb switch debouncing - time.sleep(0.1) below
        x = scroll.is_pressed(scroll.BUTTON_X)
        y = scroll.is_pressed(scroll.BUTTON_Y)
        a = scroll.is_pressed(scroll.BUTTON_A)
        b = scroll.is_pressed(scroll.BUTTON_B)

        if b:
            incr_count()
            t0 = time.time()
            save()
            plot_count()
            update()
            time.sleep(0.25)

        if a:
            decr_count()
            t0 = time.time()
            save()
            plot_count()
            update()
            time.sleep(0.25)

        if y:
            zero_count()
            t0 = time.time()
            plot_count()
            save()
            time.sleep(0.25)

        if x:
            if showing > 0:
                showing = -1
            else:
                showing = 1
            plot_count()
            save()
            time.sleep(0.25)

        update()
        time.sleep(0.02)


main()
