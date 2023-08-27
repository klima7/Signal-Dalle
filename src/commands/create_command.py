from signalbot import Command, Context

from dalle import generate_image
from translate import to_english


class CreateCommand(Command):
    def describe(self) -> str:
        return "Respond with Dall-E generated image"

    async def handle(self, c: Context):
        if c.message.base64_attachments:
            return
        
        prompt = c.message.text
        
        if not prompt:
            await c.react('🤔')
            return
        
        await c.react('👍')
        
        prompt_en = to_english(prompt)
        await c.start_typing()
        image_b64 = generate_image(prompt_en)
        await c.stop_typing()
        await c.send(
            prompt_en,
            base64_attachments=[image_b64],
        )
