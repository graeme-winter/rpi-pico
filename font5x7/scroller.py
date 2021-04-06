import time

import picoscroll as scroll

import font

scroll.init()
width = scroll.get_width()
height = scroll.get_height()


def _bin(n):
    return "{0:08b}".format(n)


def display(rendered_text, shift, brightness):
    """Display the rendered text on the scroll, at named offset"""

    assert shift >= -width
    assert shift < len(rendered_text)

    scroll.clear()

    view = rendered_text[shift : shift + width]

    for j, v in enumerate(view):
        b = _bin(v)
        for i, _b in enumerate(b):
            scroll.set_pixel(j, j, brightness)
    scroll.update()


def scroller(text, brightness):
    """Scroll the text across the screen"""

    rendered_text = font.render(text)

    for j in range(-17, len(rendered_text)):
        display(rendered_text, j, brightness)
        time.sleep(0.1)


scroller("Hello, world!", 8)
