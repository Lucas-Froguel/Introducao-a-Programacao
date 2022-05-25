import numpy as np
from PIL import Image, ImageDraw, ImageFont
from text import text

xsize, ysize = 512, 512

char = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'.            "
char = char[::-1]


def get_average_intensity(source, x=0, y=0):
    val = 0
    for c in (0, 1, 2):
        val += source[c].getpixel((x, y))

    return val / 3


def average_intensity_image(image, xsize=xsize, ysize=ysize):
    average = np.zeros((xsize, ysize))

    for x in range(xsize):
        for y in range(ysize):
            average[y, x] = np.mean(image[x, y])

    return average


def create_ascii_image_with_color(image, letter="A", xsize=xsize, ysize=ysize, save=False):
    out = Image.new("RGB", (xsize, ysize), (0, 0, 0))

    font = ImageFont.truetype("data/Verdana.ttf", 15)

    # get a drawing context
    d = ImageDraw.Draw(out)

    length = d.textbbox((10, 10), letter, font)
    xlength = length[2] - length[0]
    ylength = length[3] - length[1]

    for x in np.linspace(0, xsize-1, num=int(xsize/xlength)):
        ind_x = int(x)
        for y in np.linspace(0, ysize, num=int(ysize/ylength)):
            y = y - 5
            ind_y = int(y)
            d.text((x, y), letter, fill=image[ind_x, ind_y], font=font)

    if save:
        out.save(f"data/out-{letter}.png")

    return out


def create_ascii_image_grey(image, char=char, xsize=xsize, ysize=ysize, save=False):
    out = Image.new("RGB", (xsize, ysize), (0, 0, 0))

    font = ImageFont.truetype("data/Verdana.ttf", 15)

    # get a drawing context
    d = ImageDraw.Draw(out)

    length = d.textbbox((10, 10), "H", font)
    xlength = length[2] - length[0]
    ylength = length[3] - length[1]

    for x in np.linspace(0, xsize-1, num=int(xsize/xlength)):
        ind_x = int(x)
        for y in np.linspace(0, ysize, num=int(ysize/ylength)):
            y = y - 5
            ind_y = int(y)
            avr = np.mean(image[ind_x, ind_y]) * (len(char) / 256)
            avr = int(avr)

            # d.text((x, y), char[avr], fill=(256, 256, 256), font=font)
            d.text((x, y), char[avr], fill=image[ind_x, ind_y], font=font)

    if save:
        out.save(f"data/out_grey.png")

    return out


def create_ascii_image_with_color_and_text(image, text=text, xsize=xsize, ysize=ysize, save=False, initial_index=0):
    out = Image.new("RGB", (xsize, ysize), (0, 0, 0))

    font = ImageFont.truetype("data/Verdana.ttf", 15)

    # get a drawing context
    d = ImageDraw.Draw(out)

    length = d.textbbox((10, 10), "H", font)
    xlength = length[2] - length[0]
    ylength = length[3] - length[1]

    len_text = len(text)
    k = initial_index if initial_index < len_text else initial_index / 10

    for y in np.linspace(0, ysize, num=int(ysize / ylength)):
        y = y - 5
        ind_y = int(y)
        for x in np.linspace(0, xsize-1, num=int(xsize/xlength)):
            ind_x = int(x)

            char = text[k]
            k += 1
            if k == len_text - 1:
                k = 0

            d.text((x, y), char, fill=image[ind_x, ind_y], font=font)

    if save:
        out.save(f"data/out-text.png")

    return out


def main():
    filepath = "data/comida-mexicana-00.png"

    # Open Image
    im = Image.open(filepath)

    # Resize Image
    im = im.resize((xsize, ysize))
    im_load = im.load()

    create_ascii_image_with_color_and_text(im_load, save=True)


def get_ascii_color_from_raw_image(im):
    # Resize Image
    im = im.resize((xsize, ysize))
    im_load = im.load()

    out = create_ascii_image_with_color(im_load, letter="X")

    return out


def get_ascii_grey_from_raw_image(im):
    # Resize Image
    im = im.resize((xsize, ysize))
    im_load = im.load()

    out = create_ascii_image_grey(im_load)

    return out


def get_ascii_text_from_raw_image(im, initial_index):
    # Resize Image
    im = im.resize((xsize, ysize))
    im_load = im.load()

    out = create_ascii_image_with_color_and_text(im_load, initial_index=initial_index)

    return out


