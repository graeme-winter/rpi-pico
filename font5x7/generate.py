# generate 5x7 font bitmap as 5 bytes / char
#
# (C) Graeme Winter, 2021
#
# Encoding: each column of 7 bits is encoded top down with LSB as top ->
# horizontal line across the top is 0x01 0x01 0x01 0x01 0x01, vertical line
# on left side of box only would be 0x7f 0x00 0x00 0x00 0x00.

import sys
import urllib.request

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import inspect


def generate_bitmap():
    """Generate the bitmap from online source"""

    SOURCE = "http://sdf.org/~kt8216/font5x7/unknown-small-5x7.txt"

    tmp = {}
    with urllib.request.urlopen(SOURCE) as f:
        for j, line in enumerate(f.readlines()):
            line = line.decode().strip().replace(".", "0").replace("X", "1")
            if j < 2:
                continue
            c = (j - 2) // 8
            if not c in tmp:
                assert line[0] == "C"
                assert int(line.split()[1], 16) == c
                tmp[c] = []
                continue
            assert len(line) == 7
            tmp[c].append(line[2:7])

    bitmap = {}
    for c in sorted(tmp):
        l = []
        for j in range(5):
            r = []
            for k in range(7):
                # 6 - k to turn upside-down i.e. write bits from top down
                r.append(tmp[c][6 - k][j])
            l.append(int("".join(r), 2))
        bitmap[c] = l

    return bitmap


def render_bitmap(bitmap, filename):
    """Render font bitmap for viewing"""

    image = np.zeros(shape=(16 * 8, 16 * 6))

    for c in bitmap:
        x, y = divmod(c, 16)
        for j in range(5):
            bits = bin(bitmap[c][j])[2:].zfill(7)
            for k in range(7):
                image[8 * y + k + 1, 6 * x + j + 1] = int(bits[k])

    fig = plt.figure(figsize=(6, 8), frameon=False)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_frame_on(False)
    ax.set_xlim(0, 16 * 6)
    ax.set_ylim(16 * 8, 0)
    ax.axis("off")
    ax.imshow(image, cmap="Greys")
    plt.savefig(filename, bbox_inches="tight", pad_inches=0)


def render(text):
    """Render the text as a byte array as defined above."""

    result = bytearray()
    for t in text:
        for c in __bitmap[ord(t)]:
            result.append(c)
        result.append(0)
    return result


def display(rendered_text):
    """For debugging, print rendered text to stdout"""

    tmp = list(bin(i)[2:].zfill(7)[::-1] for i in rendered_text)
    disp = {"0": " ", "1": "*"}

    for j in range(7):
        print("".join(disp[t[j]] for t in tmp))


def save(bitmap, filename):
    """Save the generated bitmap in a format which will be useful for Python"""

    header = open("generate.py", "r").readlines()[:8]

    with open(filename, "w") as f:
        f.write("".join(header))

        f.write("__bitmap = {\n")
        for c in sorted(bitmap):
            values = ",".join(map(hex, bitmap[c]))
            f.write(f"    {hex(c)}: ({values}),\n")
        f.write("}\n")
        f.write("\n\n")
        f.write(inspect.getsource(render))
        f.write("\n\n")
        f.write(inspect.getsource(display))


def main(filename):
    matplotlib.use("Agg")
    bitmap = generate_bitmap()
    save(bitmap, filename)


if __name__ == "__main__":
    main(sys.argv[1])
