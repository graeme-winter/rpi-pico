import time
import machine

import picoscroll as scroll

from font import render

scroll.init()
width = scroll.get_width()
height = scroll.get_height()


def temperature():
    sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    return temperature


while True:
    t = str(int(round(temperature()))) + chr(26)
    b = render(t)
    scroll.show_bitmap_1d(b, 16, 0)
    scroll.update()
    time.sleep(1)
