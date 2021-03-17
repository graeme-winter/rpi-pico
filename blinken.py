import time
import random

import picoscroll as scroll

scroll.init()

width = scroll.get_width()
height = scroll.get_height()
while True:
    scroll.clear()
    for y in range(0, height):
        for x in range(0, width):
            scroll.set_pixel(x, y, 128 * int(random.random() * 2))

    scroll.update()
    time.sleep(0.2)
