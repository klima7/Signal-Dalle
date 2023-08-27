import os

from signalbot import Context
from openai import InvalidRequestError

from safe_command import SafeCommand
from dalle import generate_image
from translate import to_english, from_english
from utils import save_b64_images


class CreateCommand(SafeCommand):
    
    CREATES_COUNT = int(os.environ.get("CREATES_COUNT", 1))
    
    def describe(self) -> str:
        return "Respond with Dall-E generated image"

    async def handle_save(self, c: Context):
        prompt = c.message.text
        
        # must be text without attachments not starting with #
        if not (len(c.message.base64_attachments) == 0 and prompt and prompt[0] != '#'):
            return
        
        if not prompt:
            await c.react('🤔')
            return
        
        await c.react('👍')
        
        prompt_en = to_english(prompt)
        await c.start_typing()
        
        try:
            generated = generate_image(prompt_en)
        except InvalidRequestError:
            await c.send(from_english('Generating this content was blocked by OpenAI 😕'))
            return
        finally:
            await c.stop_typing()
        
        save_b64_images(generated, prompt)
        await c.send(
            prompt_en,
            base64_attachments=generated,
        )
