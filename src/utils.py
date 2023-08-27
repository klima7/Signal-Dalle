import os
import io
import base64
import time
from pathlib import Path

from PIL import Image
from slugify import slugify


SAVE_DIR = os.getenv("SAVE_DIR", './images')


def resize_image(image, length) -> Image:
    if image.size[0] < image.size[1]:
        resized_image = image.resize((length, int(image.size[1] * (length / image.size[0]))))
        required_loss = (resized_image.size[1] - length)
        resized_image = resized_image.crop(
            box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))
        return resized_image
    else:
        resized_image = image.resize((int(image.size[0] * (length / image.size[1])), length))
        required_loss = resized_image.size[0] - length
        resized_image = resized_image.crop(
            box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))
        return resized_image


def save_b64_images(b64_images, text):
    timestamp = time.strftime("%m-%d-%y-%H:%M:%S")
    text_slug = slugify(text)
    
    dir = Path(SAVE_DIR)
    
    for i, b64_image in enumerate(b64_images):
        image = Image.open(io.BytesIO(base64.decodebytes(bytes(b64_image, "utf-8"))))
        filename = f'{timestamp}-{text_slug}-{i}.png'
        path = dir / filename
        image.save(str(path))
