from PIL import Image
import os


def compress_image(image_in, image_out, quality=60, delete_old=False):
    img = Image.open(image_in)
    try:
        img.save(image_out, optimize=True, quality=quality)
    except OSError:
        img.convert('RGB').save(image_out, optimize=True, quality=quality)
    if delete_old:
        os.remove(image_in)
