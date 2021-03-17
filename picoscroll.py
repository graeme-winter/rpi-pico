# picoscroll emulator

__pixels = None
__WIDTH = 17
__HEIGHT = 7


def get_width():
    return __WIDTH


def get_height():
    return __HEIGHT


def init():
    global __pixels
    __pixels = dict([((x, y), 0) for x in range(__WIDTH) for y in range(__HEIGHT)])


def set_pixel(x, y, value):
    global __pixels
    assert (x, y) in __pixels
    assert value >= 0
    assert value <= 255
    __pixels[(x, y)] = value


def clear():
    global pixels
    __pixels = dict([((x, y), 0) for x in range(__WIDTH) for y in range(__HEIGHT)])


def is_pressed(button):
    return False


def update():
    global __pixels
    print(chr(27) + "[2J")
    view = ""
    for y in range(__HEIGHT):
        for x in range(__WIDTH):
            if __pixels[(x, y)] > 64:
                view += "*"
            elif __pixels[(x, y)] > 8:
                view += "."
            else:
                view += " "
        view += "\n"
    print(view)
