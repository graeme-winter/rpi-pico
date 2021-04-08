import time
import random

import picoscroll as scroll

import font

scroll.init()
width = scroll.get_width()
height = scroll.get_height()

if hasattr(scroll, "show_bitmap_1d"):

    def display(rendered_text, brightness, shift):
        scroll.show_bitmap_1d(rendered_text, brightness, shift)
        scroll.update()


else:

    def display(rendered_text, brightness, shift):
        """Display the rendered text on the scroll, at named offset"""

        assert shift >= -width
        assert shift < len(rendered_text)

        scroll.clear()

        if shift < 0:
            rendered_text = bytearray(0 for j in range(-shift)) + rendered_text
            shift = 0
        view = rendered_text[shift : shift + width]

        for j, v in enumerate(view):
            for i in range(height):
                scroll.set_pixel(j, (height - 1) - i, brightness * ((v >> i) & 1))
        scroll.update()


def scroller(text, brightness):
    """Scroll the text across the screen"""

    rendered_text = font.render(text)

    for j in range(-17, len(rendered_text)):
        display(rendered_text, brightness, j)
        time.sleep(0.1)


phrases = [
    "Hello, world!",
    "Testing, testing, 1, 2, 3",
    "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789",
]


while True:
    phrase = random.choice(phrases)
    scroller(phrase, 8)
    time.sleep(1)
