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
    image_b64 = _convert_img_array_to_bytes(image)
    mask_b64 = _convert_img_array_to_bytes(mask)
    
    response = openai.Image.create_edit(
        image=image_b64,
        mask=mask_b64,
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )
    return response['data'][0]['b64_json']


def _convert_img_array_to_bytes(img_array):
    image = Image.fromarray(img_array)
    with io.BytesIO() as output:
        image.save(output, 'PNG')
        bytes = output.getvalue()
    return bytes
