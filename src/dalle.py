import os
import io

import openai
from PIL import Image


openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )
    return response['data'][0]['b64_json']


def edit_image(image, mask, prompt):
    image_bytes = _convert_img_array_to_bytes(image)
    mask_bytes = _convert_img_array_to_bytes(mask)
    
    response = openai.Image.create_edit(
        image=image_bytes,
        mask=mask_bytes,
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )
    return response['data'][0]['b64_json']


def create_variations(image, count):
    image_bytes = _convert_img_array_to_bytes(image)
    
    response = openai.Image.create_variation(
        image=image_bytes,
        n=count,
        size="1024x1024",
        response_format="b64_json",
    )
    images = [data['b64_json'] for data in response['data']]
    return images


def _convert_img_array_to_bytes(img_array):
    image = Image.fromarray(img_array)
    with io.BytesIO() as output:
        image.save(output, 'PNG')
        bytes = output.getvalue()
    return bytes
