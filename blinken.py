import time
import random

import picoscroll as scroll

scroll.init()

width = scroll.get_width()
height = scroll.get_height()
while True:
    scroll.clear();
    for y in range(0, height):
        for x in range(0, width):
            if random.random() < 0.5:
                scroll.set_pixel(x, y, 0)
            else:
                scroll.set_pixel(x, y, 32)

    scroll.update()
    time.sleep(0.2)

