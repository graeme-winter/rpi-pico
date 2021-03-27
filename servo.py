# hardware connections:
#
# servo +5V to VSYS i.e. #39
# servo 0V to GND i.e. #38
# GPIO2 is physical pin #4 (multiple options for this)

import time
import machine

servo = machine.PWM(machine.Pin(2))
servo.freq(50)

last = 0


def moveto(angle):
    """Move servo to angle between 0, 180 degrees"""

    global last

    assert angle >= 0
    assert angle <= 180

    # approximate mapping from angle to duty cycle - also allow time to move
    # from one position to another
    duty = int((angle / 180.0) * 6400 + 2200)

    dt = 0.1 * abs(duty - last) / 1000

    last = duty

    # move to position
    servo.duty_u16(duty)

    # sleep for long enough that the move should complete
    time.sleep(0.1 + dt)

    # kill motor
    servo.duty_u16(0)


for j in range(10):
    for angle in range(0, 180, 10):
        moveto(angle)
        time.sleep(1)
    for angle in range(180, 0, -10):
        moveto(angle)
        time.sleep(1)
