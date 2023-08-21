import os

import openai


openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )
    return response['data'][0]['b64_json']
