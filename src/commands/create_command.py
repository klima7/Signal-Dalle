import os

from signalbot import Command, Context

from dalle import generate_image
from translate import to_english
from utils import save_b64_images


class CreateCommand(Command):
    
    CREATES_COUNT = int(os.environ.get("CREATES_COUNT", 1))
    
    def describe(self) -> str:
        return "Respond with Dall-E generated image"

    async def handle(self, c: Context):
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
        generated = generate_image(prompt_en)
        save_b64_images(generated, prompt)
        await c.stop_typing()
        await c.send(
            prompt_en,
            base64_attachments=generated,
        )
